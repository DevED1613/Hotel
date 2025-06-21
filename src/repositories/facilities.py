
from sqlalchemy import delete, insert, select

from src.schemas.facilities import Facility, RoomFacilityAdd
from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepository

class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility
    

class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacilityAdd

    async def update_facilities(self, room_id: int, data: set[BaseModel]) -> None: # type: ignore
        tmp = select(self.model.facility_id).filter(self.model.room_id == room_id)
        res = await self.session.execute(tmp)
        current_facilities = set(res.scalars().all())
        delete_stmt = current_facilities - data
        insert_stmt = data - current_facilities

        if delete_stmt:
            delete_stmt = delete(self.model).filter(self.model.room_id == room_id).filter(self.model.facility_id.in_(delete_stmt))
            await self.session.execute(delete_stmt)
        if insert_stmt:
            insert_stmt = insert(self.model).values([{"room_id": room_id, "facility_id": f_id} for f_id in insert_stmt])
            await self.session.execute(insert_stmt)

        await self.session.commit()




        