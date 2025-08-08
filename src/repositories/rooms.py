from datetime import date

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload

from src.exceptions import RoomNotFoundException
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RoomDataMapper, RoomWithFacilDataMapper
from src.repositories.utils import rooms_id_for_booking


class RoomsRepository(BaseRepository):
    model: type[RoomsOrm] = RoomsOrm
    mapper = RoomDataMapper

    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):
        # проверка на корректность id отеля
        hotel_check = select(HotelsOrm).filter_by(id=hotel_id)
        result = await self.session.execute(hotel_check)
        try:
            result.scalars().one()
        except NoResultFound:
            raise RoomNotFoundException

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

    async def get_one_with_facilities(self, **filter_by) -> BaseModel | None:
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )

        result = await self.session.execute(query)
        try:
            model = result.scalars().one()
        except NoResultFound:
            raise RoomNotFoundException
        return RoomWithFacilDataMapper.map_to_domain_entity(model)
