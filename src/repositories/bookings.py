from datetime import date

from fastapi import HTTPException
from sqlalchemy import insert, select

from src.schemas.bookings import BookingAdd
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.repositories.utils import rooms_id_for_booking


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_booking_for_today_checkin(self):
        query = select(self.model).where(self.model.date_from == date.today())
        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(model) for model in result.scalars().all()
        ]

    async def add_booking(self, data: BookingAdd, hotel_id: int):
        rooms_query = rooms_id_for_booking(
            data.date_from, data.date_to, hotel_id=hotel_id
        )

        result = await self.session.execute(rooms_query)
        free_room_ids: list[int] = result.scalars().all()

        if not free_room_ids or data.room_id not in free_room_ids:
            raise HTTPException(status_code=400, detail="Room not available")

        
        if data.room_id in free_room_ids:
            new_booking = await self.add(data)
            return new_booking
        else:
            raise Exception
