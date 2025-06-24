from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.repositories.mappers.mappers import RoomDataMapper, RoomWithFacilDataMapper
from src.repositories.utils import rooms_id_for_booking

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDataMapper

    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):
        rooms_id_to_get = rooms_id_for_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(self.model.id.in_(rooms_id_to_get))
        )
        result = await self.session.execute(query)

        return [
            RoomWithFacilDataMapper.map_to_domain_entity(model)
            for model in result.unique().scalars().all()
        ]

    async def get_one_or_none(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )

        result = await self.session.execute(query)
        model = result.scalars().unique().one_or_none()
        if model is None:
            return None
        return [RoomWithFacilDataMapper.map_to_domain_entity(model)]
