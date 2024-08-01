from database.service import get_all_open_campaigns


def get_all_campaigns():
    campaigns = get_all_open_campaigns()
    return campaigns
