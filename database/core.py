import sqlite3
from enum import Enum
from typing import Literal, List

from sqlalchemy import create_engine, text, String, CheckConstraint, DateTime, BigInteger, PickleType
from sqlalchemy.orm import Session, declarative_base, mapped_column, Mapped, validates

Base = declarative_base()
engine = create_engine("sqlite:///database/drops.db") # prod

# engine = create_engine("sqlite:///drops.db")

print('exec core')

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


Base.metadata.create_all(engine)

session = Session(engine)

