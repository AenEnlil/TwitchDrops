from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from .exceptions import UserAlreadyExistException
from .schemas import UserCreateSchema
from .service import create_user_in_db
from ..messages import NOT_FOUND, USER_ALREADY_EXIST

router = APIRouter(
    prefix='/users',
    tags=["users"],
    responses={404: {"description": NOT_FOUND}},
)


@router.post('/', status_code=status.HTTP_200_OK, name='users:create')
async def create_user(user: UserCreateSchema):
    try:
        create_user_in_db(user.model_dump())
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder({'result': 'user successfully created'}))
    except UserAlreadyExistException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=USER_ALREADY_EXIST)
