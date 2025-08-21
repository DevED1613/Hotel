from pydantic import BaseModel, Field

from src.schemas.base import BaseSchema


class HotelAdd(BaseSchema):
    title: str
    location: str


class Hotel(HotelAdd):
    id: int


class HotelPatch(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)

    class Config:
        from_attributes = True
