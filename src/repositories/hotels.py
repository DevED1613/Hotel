from datetime import date
from sqlalchemy import select


from src.repositories.mappers.mappers import HotelDataMapper
from src.models.rooms import RoomsOrm
from src.repositories.utils import rooms_id_for_booking
from src.schemas.hotels import Hotel
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    mapper = HotelDataMapper

    async def get_filtered_by_time(
        self,
        date_from: date,
        date_to: date,
        location: str,
        title: str,
        limit: int,
        offset: int,
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

        return [
            self.mapper.map_to_domain_entity(model) for model in result.scalars().all()
        ]
