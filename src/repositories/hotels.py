from datetime import date
from sqlalchemy import select

from src.models.rooms import RoomsOrm
from src.repositories.utils import rooms_id_for_booking
from src.schemas.hotels import Hotel
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_all(self, location, title, limit, offset) -> list[Hotel]:
        query = select(self.model)
        if title:
            query = query.where(self.model.title.ilike(f"%{title}%"))
        if location:
            query = query.where(self.model.location.ilike(f"%{location}%"))
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

    async def get_filtered_by_time(
            self,
            date_from : date, 
            date_to : date,
            location: str,
            title: str,
            limit: int,
            offset: int
    ) -> list[Hotel]:
        
        rooms_id_to_get = rooms_id_for_booking(date_from=date_from, date_to=date_to)
        hotels_id_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_id_to_get))
        )

        query = select(self.model).filter(self.model.id.in_(hotels_id_to_get))
        if title:
            query = query.where(self.model.title.ilike(f"%{title}%"))
        if location:
            query = query.where(self.model.location.ilike(f"%{location}%"))

        query = query.limit(limit).offset(offset)
           
        result = await self.session.execute(query)
        
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]