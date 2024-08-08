from typing import List

from sqlalchemy import String, CheckConstraint, DateTime, BigInteger, PickleType
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

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
    rewards: Mapped[List] = mapped_column(PickleType(), default=[])


class Users(Base):

    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    subscribed_games: Mapped[List] = mapped_column(PickleType(), default=[])
