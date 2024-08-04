from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    user_id: int
