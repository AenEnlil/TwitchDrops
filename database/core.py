from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from database.tables import Base

engine = create_engine("sqlite:///database/drops.db") # prod

# engine = create_engine("sqlite:///drops.db")

print('exec core')

Base.metadata.create_all(engine)

db_session = Session(engine)

