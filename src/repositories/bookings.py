from datetime import date

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import insert, select
from sqlalchemy.orm import selectinload

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

    async def add_booking(self, data: BaseModel):
        rooms_query = rooms_id_for_booking(data.date_from, data.date_to, data.hotel_id)

        result = await self.session.execute(rooms_query)
        free_room_ids = result.scalars().all()

        if not free_room_ids or data.room_id not in free_room_ids:
            raise HTTPException(status_code=400, detail="Room not available")

        add_data_stmt = (
            insert(self.model).values(**data.model_dump()).returning(self.model)
        )
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().first()

        if not model:
            raise HTTPException(status_code=500, detail="Failed to create booking")
        return self.mapper.map_to_domain_entity(model)
