from enum import Enum
from datetime import datetime
from sqlalchemy import text, select

from database.core import session, engine, Campaigns


class TableNamesMap(Enum):
    campaigns = Campaigns


test_data = [{
        "game": "Dawntrail Twitch Viewer Rewards Campaign: Chocorpokkur Whistle (Mount) x1",
        "company": "Square Enix",
        "campaign_name": "Summary",
        "status": "open",
        'start_date': datetime.strptime('Tue, Jul 2, 11:00 AM', '%a, %b %d, %I:%M %p'),
        'end_date': datetime.strptime('Mon, Jul 29, 11:00 AM', '%a, %b %d, %I:%M %p')
},
    {
        "game": "World of Tanks Console",
        "company": "Wargaming",
        "campaign_name": "Patriots Season Week 9",
        "status": 'closed',
        'start_date': datetime.strptime('Tue, Jul 16, 1:00 PM', '%a, %b %d, %I:%M %p'),
        'end_date': datetime.strptime('Tue, Jul 23, 11:58 AM', '%a, %b %d, %I:%M %p')
    }]


def prepare_data_to_save(tablename, data: list):
    data_ready_to_save = [tablename(**item) for item in data]
    return data_ready_to_save


def save_to_database(tablename, data):
    print(engine.pool.status())
    prepared_data = prepare_data_to_save(tablename, data)

    session.add_all(prepared_data)
    session.commit()
    print(engine.pool.status())

# save_to_database(TableNamesMap.campaigns.value, test_data)

