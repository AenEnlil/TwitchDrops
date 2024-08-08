from sqlalchemy.exc import IntegrityError

from api.users.exceptions import UserAlreadyExistException
from database.service import save_to_database, TableNamesMap, get_user_subscribed_games, \
    update_user_subscribed_games
from database.core import db_session


def create_user_in_db(user_data):
    try:
        save_to_database(db_session, TableNamesMap.users.value, [user_data])
    except IntegrityError:
        db_session.rollback()
        raise UserAlreadyExistException


def clear_duplicates(subscribed_games: int, new_games: list):
    cleared_games = [game.get('game') for game in new_games if game.get('game') not in subscribed_games]
    return cleared_games


def subscribe_to_games(user_id: int, games: list):
    subscribed_games = get_user_subscribed_games(db_session, user_id)
    cleared_games = clear_duplicates(subscribed_games, games)
    subscribed_games.extend(cleared_games)

    update_user_subscribed_games(db_session, user_id, subscribed_games)
