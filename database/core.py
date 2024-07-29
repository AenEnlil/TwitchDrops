import sqlite3
from enum import Enum
from typing import Literal

from sqlalchemy import create_engine, text, String, CheckConstraint
from sqlalchemy.orm import Session, declarative_base, mapped_column, Mapped, validates

Base = declarative_base()
# engine = create_engine("sqlite:///database/drops.db") #prod

engine = create_engine("sqlite:///drops.db")

print('exec core')

status_validation = "status == 'open' or status == 'closed'"


class Campaigns(Base):

    __tablename__ = "campaigns"

    id: Mapped[int] = mapped_column(primary_key=True)
    game: Mapped[str] = mapped_column(String(60))
    company: Mapped[str] = mapped_column(String(60))
    campaign_dates: Mapped[str] = mapped_column(String(120))
    campaign_name: Mapped[str] = mapped_column(String(60))
    status: Mapped[str] = mapped_column(String(10), CheckConstraint(status_validation))


Base.metadata.create_all(engine)

session = Session(engine)

