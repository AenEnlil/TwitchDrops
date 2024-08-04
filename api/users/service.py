from sqlalchemy.exc import IntegrityError

from api.users.exceptions import UserAlreadyExistException
from database.service import save_to_database, TableNamesMap, session


def create_user_in_db(user_data):
    try:
        save_to_database(TableNamesMap.users.value, [user_data])
    except IntegrityError:
        session.rollback()
        raise UserAlreadyExistException
