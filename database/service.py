from enum import Enum

from sqlalchemy import text, select

from database.core import session, engine, Campaigns


class TableNamesMap(Enum):
    campaigns = Campaigns


d = [{
    "game": "Dawntrail Twitch Viewer Rewards Campaign: Chocorpokkur Whistle (Mount) x1",
    "company": "Square Enix",
    "campaign_dates": "Tue, Jul 2, 11:00 AM GMT+3 - Mon, Jul 29, 11:00 AM GMT+3",
    "campaign_name": "Summary",
    "status": "asd"
}]

c = [{
    "game": "Avatar: Frontiers of Pandora",
    "company": "Ubisoft",
    "campaign_dates": "Tue, Jul 16, 11:00 AM - Tue, Jul 23, 9:58 PM GMT+3",
    "campaign_name": "Avatar : Frontiers Of Pandora - July 2024",
    "status": 'open'
},
    {
        "game": "World of Tanks Console",
        "company": "Wargaming",
        "campaign_dates": "Tue, Jul 16, 1:00 PM - Tue, Jul 23, 11:58 AM GMT+3",
        "campaign_name": "Patriots Season Week 9",
        "status": 'closed'
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

# save_to_database(TableNamesMap.campaigns.value, c)
