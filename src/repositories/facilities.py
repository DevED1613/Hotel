from pydantic import BaseModel
from sqlalchemy import delete, insert, select

from src.repositories.mappers.mappers import (
    FacilitiesDataMapper,
    RoomFacilityDataMapper,
)
from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepository


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    mapper = FacilitiesDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    mapper = RoomFacilityDataMapper

    async def update_facilities(self, room_id: int, data: list[BaseModel]) -> None:
        update_data_stmt = {item.facility_id for item in data}
        tmp = select(self.model.facility_id).filter(self.model.room_id == room_id)
        res = await self.session.execute(tmp)
        current_facilities = set(res.scalars().all())
        delete_stmt = current_facilities - update_data_stmt
        insert_stmt = update_data_stmt - current_facilities

        if delete_stmt:
            delete_stmt = (
                delete(self.model)
                .filter(self.model.room_id == room_id)
                .filter(self.model.facility_id.in_(delete_stmt))
            )
            await self.session.execute(delete_stmt)
        if insert_stmt:
            insert_stmt = insert(self.model).values(
                [{"room_id": room_id, "facility_id": f_id} for f_id in insert_stmt]
            )
            await self.session.execute(insert_stmt)
