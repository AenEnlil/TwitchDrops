from datetime import datetime
from typing import List

import pytest
from sqlalchemy import create_engine, String, CheckConstraint, DateTime, BigInteger, PickleType, select
from sqlalchemy.orm import Session, declarative_base, Mapped, mapped_column

Base = declarative_base()

status_validation = "status == 'open' or status == 'closed'"


class Campaigns(Base):

    __tablename__ = "campaigns"

    id: Mapped[int] = mapped_column(primary_key=True)
    game: Mapped[str] = mapped_column(String(60))
    company: Mapped[str] = mapped_column(String(60))
    campaign_name: Mapped[str] = mapped_column(String(60))
    status: Mapped[str] = mapped_column(String(10), CheckConstraint(status_validation))
    start_date: Mapped[str] = mapped_column(DateTime)
    end_date: Mapped[str] = mapped_column(DateTime)


class Users(Base):

    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    subscribed_games: Mapped[List] = mapped_column(PickleType(), default=[])


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
        'end_date': datetime.strptime('Mon, Jul 29, 11:00 AM', '%a, %b %d, %I:%M %p')
},
    {
        "game": "Rise Online",
        "company": "Roko Game Studios",
        "campaign_name": "ROW - Twitch Drop 114",
        'start_date': datetime.strptime('Tue, Jul 31, 1:00 PM', '%a, %b %d, %I:%M %p'),
        'end_date': datetime.strptime('Tue, Aug 23, 11:58 AM', '%a, %b %d, %I:%M %p'),
        "status": "open"
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


