from collections import defaultdict

from bot.notification import notify_users_about_new_campaign
from database.service import get_all_open_campaigns, get_campaigns_by_game, get_user_subscribed_games, \
    get_users_subscribed_for_game
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


def group_campaigns_by_game(campaigns: list):
    campaigns_grouped_by_game = defaultdict(list)

    for campaign in campaigns:
        campaigns_grouped_by_game[campaign.get('game')].append(campaign)

    return campaigns_grouped_by_game


async def notify_users_about_new_campaigns(campaigns: list):
    games = {campaign.get('game') for campaign in campaigns}
    campaigns_grouped_by_game = group_campaigns_by_game(campaigns)

    for game in games:
        users = get_users_subscribed_for_game(db_session, game)

        if users:
            user_ids = [user.get('user_id') for user in users]
            game_campaigns = campaigns_grouped_by_game.get(game)
            await notify_users_about_new_campaign(user_ids, game_campaigns)

