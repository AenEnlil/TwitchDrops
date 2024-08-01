from enum import Enum
from datetime import datetime
from sqlalchemy import text, select

from database.core import session, engine, Campaigns


class TableNamesMap(Enum):
    campaigns = Campaigns


duplicate_filter_columns_selector = {
        TableNamesMap.campaigns.value: [Campaigns.campaign_name, Campaigns.game,
                                        Campaigns.start_date, Campaigns.end_date]
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
    data_ready_to_save = [tablename(**item) for item in data]
    return data_ready_to_save


def remove_duplicates(tablename, data: list) -> list:
    columns = duplicate_filter_columns_selector.get(tablename)
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


def save_to_database(tablename, data, exclude_duplicates=False):
    # TODO: maybe move duplicates handling to scrap part
    print(engine.pool.status())

    if exclude_duplicates:
        data = remove_duplicates(tablename, data)

    prepared_data = prepare_data_to_save(tablename, data)

    session.add_all(prepared_data)
    session.commit()
    print(engine.pool.status())


def get_all_open_campaigns():
    """ doc """
    '''
        _asdict method and _mapping property only work for Row objects from session execute with
        select query that looks for certain columns(select(Campaigns.company, Campaigns,status))
        __dict__ works for Table object (in Row objects)
    '''
    statement = select(Campaigns.campaign_name, Campaigns.game,
                       Campaigns.start_date, Campaigns.end_date).filter_by(status='open')
    query_result = session.execute(statement).all()

    campaigns = [item._asdict() for item in query_result]
    return campaigns

# save_to_database(TableNamesMap.campaigns.value, test_data, exclude_duplicates=True)
# get_all_open_campaigns()
# remove_duplicates(TableNamesMap.campaigns.value, test_data)

