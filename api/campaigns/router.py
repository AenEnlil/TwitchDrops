from typing import List

from fastapi import APIRouter, HTTPException
from starlette import status

from .exceptions import NoSubscribedGamesExceptions
from .service import get_all_campaigns, get_subscribed_campaigns, notify_users_about_new_campaigns
from .schemas import CampaignResponseSchema
from ..messages import NOT_FOUND, NO_SUBSCRIBED_GAMES

router = APIRouter(
    prefix='/campaigns',
    tags=["campaigns"],
    responses={404: {"description": NOT_FOUND}},
)


@router.get('/all', status_code=status.HTTP_200_OK, name='campaigns:all_campaigns',
            response_model=List[CampaignResponseSchema])
async def get_all_drop_campaigns():
    campaigns = get_all_campaigns()
    return campaigns


@router.get('/subscribed', status_code=status.HTTP_200_OK, name='campaigns:subscribed',
            response_model=List[CampaignResponseSchema])
async def get_campaigns_by_subscribed_games(user_id: int):
    try:
        campaigns = get_subscribed_campaigns(user_id)
        return campaigns
    except NoSubscribedGamesExceptions:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=NO_SUBSCRIBED_GAMES)


@router.post('/notify-users', status_code=status.HTTP_200_OK, name='campaigns:notify')
async def notify_about_new_campaigns(campaigns: List[CampaignResponseSchema]):
    dumped_campaigns = [item.model_dump() for item in campaigns]
    await notify_users_about_new_campaigns(dumped_campaigns)

