from src.schemas.bookings import BookingAdd, BookingAddRequst
from src.services.base import BaseService, DataCheckService


class BookingService(BaseService):
    async def get_all_bookings(self):
        return await self.db.bookings.get_all()

    async def get_user_bookings(self, user_id: int):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def add_booking(self, booking_data: BookingAddRequst, user_id: int):
        DataCheckService.check_date_to_after_date_from(
            date_from=booking_data.date_from, date_to=booking_data.date_to
        )

        room = await DataCheckService.check_room_exists(
            db=self.db,
            room_id=booking_data.room_id,
        )

        price_room: int = room.price  # type: ignore
        _booking_data = BookingAdd(
            user_id=user_id, price=price_room, **booking_data.model_dump()
        )

        booking = await self.db.bookings.add_booking(
            _booking_data, hotel_id=room.hotel_id
        )

        await self.db.commit()

        return booking
