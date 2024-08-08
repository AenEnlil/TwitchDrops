from datetime import datetime

import pytest
from sqlalchemy import select

from database.service import prepare_data_to_save, remove_duplicates, save_to_database, get_all_open_campaigns, \
    get_campaigns_by_game, get_user_subscribed_games, update_user_subscribed_games
from database.exceptions import DuplicateFilterError
from tests.conftest import database_session, Users, Campaigns, test_campaigns

user_with_valid_data = {"user_id": 1234,
                        "subscribed_games": ['Game1', 'Game2']}
campaigns_with_valid_data = [{
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


def test_prepare_data_to_save():
    data = prepare_data_to_save(Users, [user_with_valid_data])

    assert data
    assert type(data[0] == Users)


def test_remove_duplicates_for_not_configured_table(database_session):
    data = [{"user_id": 1234, "subscribed_games": ['Game1', 'Game2']},
            {"user_id": 4321, "subscribed_games": ['Game1', 'Game2']}]

    with pytest.raises(DuplicateFilterError):
        remove_duplicates(database_session, Users, data)


def test_remove_duplicates(database_session):
    existing_company = test_campaigns[0]
    data = campaigns_with_valid_data.copy()
    data.append(existing_company)

    assert campaigns_with_valid_data[0] in data
    assert existing_company in data

    cleared_data = remove_duplicates(database_session, Campaigns, data)
    assert len(cleared_data) != len(data)
    assert existing_company not in cleared_data


def test_save_to_database(database_session):
    statement = select(Campaigns.game, Campaigns.campaign_name)
    query_result_before_add = database_session.execute(statement).all()

    data = campaigns_with_valid_data
    save_to_database(database_session, Campaigns, data)

    query_result_before_after_add = database_session.execute(statement).all()

    assert len(query_result_before_add) != len(query_result_before_after_add)


def test_get_all_open_campaigns(database_session):
    campaigns = get_all_open_campaigns(database_session)

    assert campaigns
    assert campaigns[0]['campaign_name'] == test_campaigns[0]['campaign_name']


def test_get_campaigns_by_games(database_session):
    statement = select(Campaigns.campaign_name, Campaigns.game,
                       Campaigns.start_date, Campaigns.end_date).filter_by(status='open')
    query_result = database_session.execute(statement).all()
    existing_campaigns = [item._asdict() for item in query_result]
    assert existing_campaigns

    campaign = existing_campaigns[0]
    campaigns_by_game = get_campaigns_by_game(database_session, [campaign.get('game')])

    assert len(campaigns_by_game) != len(existing_campaigns)
    assert campaign in campaigns_by_game


def test_get_user_subscribed_games(database_session):
    statement = select(Users.user_id, Users.subscribed_games)
    users = database_session.execute(statement).all()

    assert users

    user = users[0]._asdict()
    user_games = get_user_subscribed_games(database_session, user.get('user_id'))

    assert user_games
    assert user_games == user.get('subscribed_games')


def test_update_user_subscribed_games(database_session):
    statement = select(Users.user_id, Users.subscribed_games)
    users = database_session.execute(statement).all()

    assert users

    user = users[0]._asdict()
    data = user.get('subscribed_games').copy()
    data.append('New Game')

    update_user_subscribed_games(database_session, user.get('user_id'), data)
    updated_users = database_session.execute(statement).all()

    assert updated_users

    updated_user = updated_users[0]._asdict()

    assert updated_user.get('user_id') == user.get('user_id')
    assert updated_user.get('subscribed_games') != user.get('subscribed_games')
    assert 'New Game' in updated_user.get('subscribed_games')
