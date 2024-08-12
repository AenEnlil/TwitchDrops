from enum import Enum
from datetime import datetime
from sqlalchemy import text, select, delete

from database.tables import Campaigns, Users
from database.exceptions import DuplicateFilterError

# TODO: for methods that accept tablename add check if given tablename exist


class TableNamesMap(Enum):
    campaigns = Campaigns
    users = Users


duplicate_filter_columns_selector = {
        TableNamesMap.campaigns.value: [Campaigns.campaign_name, Campaigns.game,
                                        Campaigns.start_date, Campaigns.end_date],
}


test_data = [{
        "game": "Dawntrail Twitch Viewer Rewards Campaign: Chocorpokkur Whistle (Mount) x1",
        "company": "Square Enix",
        "campaign_name": "Summary",
        "status": "open",
        'start_date': datetime.strptime('Tue, Jul 2, 11:00 AM', '%a, %b %d, %I:%M %p'),
        'end_date': datetime.strptime('Mon, Jul 29, 11:00 AM', '%a, %b %d, %I:%M %p')
},
    {
        "game": "Rise Online",
        "company": "Roko Game Studios",
        "campaign_name": "ROW - Twitch Drop 114",
        'start_date': datetime.strptime('Tue, Jul 31, 1:00 PM', '%a, %b %d, %I:%M %p'),
        'end_date': datetime.strptime('Tue, Aug 23, 11:58 AM', '%a, %b %d, %I:%M %p'),
        "status": "open"
    },
    {
        "game": "Stormgate",
        "company": "Frost Giant Studios",
        "campaign_name": "Stormgate Early Access Launch Drops",
        'start_date': datetime.strptime('Tue, Jul 31, 1:00 PM', '%a, %b %d, %I:%M %p'),
        'end_date': datetime.strptime('Tue, Aug 23, 11:58 AM', '%a, %b %d, %I:%M %p'),
        "status": "open"
    },
    {
        "game": "STALCRAFT: X",
        "company": "EXBO",
        "campaign_name": "BS 2",
        'start_date': datetime.strptime('Tue, Jul 31, 1:00 PM', '%a, %b %d, %I:%M %p'),
        'end_date': datetime.strptime('Tue, Aug 23, 11:58 AM', '%a, %b %d, %I:%M %p'),
        "status": "open"
    },
    {
        "game": "Wakfu",
        "company": "ANKAMA Games",
        "campaign_name": "Viewer Box Necroworld J6",
        'start_date': datetime.strptime('Tue, Jul 31, 1:00 PM', '%a, %b %d, %I:%M %p'),
        'end_date': datetime.strptime('Tue, Aug 23, 11:58 AM', '%a, %b %d, %I:%M %p'),
        "status": "open"
    },
    {
        "game": "World of Tanks Console",
        "company": "Wargaming",
        "campaign_name": "Patriots Season Week 9",
        "status": 'closed',
        'start_date': datetime.strptime('Tue, Jul 16, 1:00 PM', '%a, %b %d, %I:%M %p'),
        'end_date': datetime.strptime('Tue, Jul 23, 11:58 AM', '%a, %b %d, %I:%M %p')
    }]


def prepare_data_to_save(tablename, data: list) -> list:
    """
    Converts every dict item in data list to tablename instance

    :param tablename: Table class which will be used to create instances of it
    :param data: list of data that will be converted to Table instances
    :return: list of Table instances that represents rows of Table
    """
    data_ready_to_save = [tablename(**item) for item in data]
    return data_ready_to_save


def remove_duplicates(session, tablename, data: list) -> list:
    columns = duplicate_filter_columns_selector.get(tablename)
    if not columns:
        raise DuplicateFilterError

    columns_as_keys = [column.key for column in columns]
    statement = select(*columns).filter_by(status='open')

    query_result = session.execute(statement).all()
    data_from_database = [item._asdict() for item in query_result]

    data_with_filtered_keys = [{k: v for k, v in data_item.items() if k in columns_as_keys} for data_item in data]

    data_without_duplicates = []
    for index, item in enumerate(data_with_filtered_keys):
        if item not in data_from_database:
            data_without_duplicates.append(data[index])
    return data_without_duplicates


def save_to_database(session, tablename, data):
    prepared_data = prepare_data_to_save(tablename, data)

    session.add_all(prepared_data)
    session.commit()


def get_all_open_campaigns(session):
    """ doc """
    '''
        _asdict method and _mapping property only work for Row objects from session execute with
        select query that looks for certain columns(select(Campaigns.company, Campaigns,status))
        __dict__ works for Table object (in Row objects)
    '''
    statement = select(Campaigns.campaign_name, Campaigns.game,
                       Campaigns.start_date, Campaigns.end_date, Campaigns.rewards).filter_by(status='open')
    query_result = session.execute(statement).all()

    campaigns = [item._asdict() for item in query_result]
    return campaigns


def get_campaigns_by_game(session, games: list):
    statement = select(Campaigns.campaign_name, Campaigns.game,
                       Campaigns.start_date, Campaigns.end_date, Campaigns.rewards).filter(Campaigns.game.in_(games))
    query_result = session.execute(statement).all()

    campaigns = [item._asdict() for item in query_result]
    return campaigns


def get_user_subscribed_games(session, user_id: int):
    statement = select(Users.subscribed_games).filter_by(user_id=user_id)
    query_result = session.scalars(statement).all()
    return query_result[0] if query_result else query_result


def update_user_subscribed_games(session, user_id: int, subscribed_games: list):
    session.query(Users).filter_by(user_id=user_id).update({"subscribed_games": subscribed_games})
    session.commit()


def close_ended_campaigns(session):
    current_date = datetime.now()
    statement = select(Campaigns.id, Campaigns.game, Campaigns.end_date, Campaigns.status).filter_by(status='open')

    query_result = session.execute(statement).all()
    campaigns = [item._asdict() for item in query_result]
    ended_campaigns_id = [campaign.get('id') for campaign in campaigns if campaign.get('end_date') < current_date]

    if ended_campaigns_id:
        session.query(Campaigns).filter(Campaigns.id.in_(ended_campaigns_id)).update({'status': 'closed'})
        session.commit()


def delete_ended_campaigns(session):
    statement = select(Campaigns.id).filter_by(status='closed')

    query_result = session.execute(statement).all()
    closed_campaigns = [item._asdict() for item in query_result]
    ended_campaigns_id = [campaign.get('id') for campaign in closed_campaigns]

    if ended_campaigns_id:
        session.query(Campaigns).filter(Campaigns.id.in_(ended_campaigns_id)).delete()
        session.commit()
