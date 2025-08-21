from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.schemas.base import BaseSchema
from src.schemas.facilities import Facility


class RoomAdd(BaseSchema):
    hotel_id: int
    title: str
    description: str | None = Field(None)
    price: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)

    @field_validator("description")
    @classmethod
    def skip_empty(cls, value: str | None) -> str | None:
        return value


class RoomAddRequest(BaseSchema):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] | None = Field(None)

    @field_validator("description")
    @classmethod
    def skip_empty(cls, value: str | None) -> str | None:
        return value


class Room(RoomAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class RoomWithFacilities(Room):
    facilities: list[Facility]


class RoomPatch(BaseModel):
    hotel_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = Field(None, gt=0)
    quantity: int | None = Field(None, gt=0)


class RoomPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facilities_ids: list[int] | None = None
