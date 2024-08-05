from database.service import get_all_open_campaigns, get_campaigns_by_game, get_user_subscribed_games


def get_all_campaigns():
    campaigns = get_all_open_campaigns()
    return campaigns


def get_subscribed_campaigns(user_id: int):
    subscribed_games = get_user_subscribed_games(user_id)
    campaigns = get_campaigns_by_game(subscribed_games)
    return campaigns
