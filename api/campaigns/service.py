from database.service import get_all_open_campaigns, get_campaigns_by_game, get_user_subscribed_games
from database.core import db_session

from api.campaigns.exceptions import NoSubscribedGamesExceptions


def get_all_campaigns():
    campaigns = get_all_open_campaigns(db_session)
    return campaigns


def get_subscribed_campaigns(user_id: int):
    subscribed_games = get_user_subscribed_games(db_session, user_id)
    if not subscribed_games:
        raise NoSubscribedGamesExceptions
    campaigns = get_campaigns_by_game(db_session, subscribed_games)
    return campaigns
