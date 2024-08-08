from datetime import datetime
from typing import List

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from database.tables import Base, Users, Campaigns


test_user = {
    "user_id": 1,
    "subscribed_games": ['Rise Online', 'Dota 2']
}

test_campaigns = [{
        "game": "Dawntrail Twitch Viewer Rewards Campaign: Chocorpokkur Whistle (Mount) x1",
        "company": "Square Enix",
        "campaign_name": "Summary",
        "status": "open",
        'start_date': datetime.strptime('Tue, Jul 2, 11:00 AM', '%a, %b %d, %I:%M %p'),
        'end_date': datetime.strptime('Mon, Jul 29, 11:00 AM', '%a, %b %d, %I:%M %p'),
        'rewards': ['Reward1']
},
    {
        "game": "Rise Online",
        "company": "Roko Game Studios",
        "campaign_name": "ROW - Twitch Drop 114",
        'start_date': datetime.strptime('Tue, Jul 31, 1:00 PM', '%a, %b %d, %I:%M %p'),
        'end_date': datetime.strptime('Tue, Aug 23, 11:58 AM', '%a, %b %d, %I:%M %p'),
        "status": "open",
        'rewards': ['Reward1', 'Reward2']
    }]


@pytest.fixture
def database_session():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    session = Session(engine)

    session.add(Users(**test_user))
    for campaign in test_campaigns:
        session.add(Campaigns(**campaign))
    session.commit()

    yield session

    session.close()


