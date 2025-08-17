from pydantic import BaseModel, ConfigDict

from src.schemas.base import BaseSchema


class FacilityAdd(BaseSchema):
    title: str


class Facility(FacilityAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomFacilityAdd(BaseModel):
    room_id: int
    facility_id: int


class RoomFacility(RoomFacilityAdd):
    id: int
