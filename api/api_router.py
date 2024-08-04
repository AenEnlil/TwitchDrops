from fastapi import APIRouter
from starlette.responses import JSONResponse

from .campaigns import router as campaigns_router
from .users import router as users_router

api_router = APIRouter(
    default_response_class=JSONResponse,
)

api_router.include_router(campaigns_router.router)
api_router.include_router(users_router.router)

