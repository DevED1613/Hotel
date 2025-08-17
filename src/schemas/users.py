from pydantic import BaseModel, ConfigDict, EmailStr

from src.schemas.base import BaseSchema


class UserRequestAdd(BaseSchema):
    email: EmailStr
    password: str


class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str


class User(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserInDB(User):
    hashed_password: str
