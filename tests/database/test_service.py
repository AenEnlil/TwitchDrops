from datetime import datetime

import pytest
from sqlalchemy import text, select

from database.service import prepare_data_to_save, remove_duplicates
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


def test_remove_duplicates_for_not_configured_table():
    data = [{"user_id": 1234, "subscribed_games": ['Game1', 'Game2']},
            {"user_id": 4321, "subscribed_games": ['Game1', 'Game2']}]

    with pytest.raises(DuplicateFilterError):
        remove_duplicates(Users, data)


# def test_remove_duplicates():
#     existing_company = test_campaigns[0]
#     data = campaigns_with_valid_data.copy()
#     data.append(existing_company)
#
#     assert campaigns_with_valid_data[0] in data
#     assert existing_company in data

    # cleared_data = remove_duplicates(Campaigns, data)
    # print(cleared_data)


# def test_a(database_session):
    # print(database_session.execute(text('SHOW TABLES')))

    # database_session.add(Users(user_id=1, subscribed_games=['ASd']))
    # database_session.commit()

    # statement = select(Users.user_id, Users.subscribed_games)
    # query_result = database_session.execute(statement).all()
    # print(query_result)

    # statement = select(Campaigns.game, Campaigns.campaign_name)
    # query_result = database_session.execute(statement).all()
    # print(query_result)


# def test_b(database_session):
    # print(3)
    # statement = select(Users.user_id, Users.subscribed_games)
    # query_result = database_session.execute(statement).all()
    # print(query_result)
    # print(database_session.query(Campaigns).all())