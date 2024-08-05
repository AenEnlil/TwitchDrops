from typing import List

from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse

from .service import get_all_campaigns, get_subscribed_campaigns
from .schemas import CampaignResponseSchema
from ..messages import NOT_FOUND


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
    campaigns = get_subscribed_campaigns(user_id)
    return campaigns
