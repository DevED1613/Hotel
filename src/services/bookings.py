from src.exceptions import NoAvailableRoomsException
from src.schemas.bookings import BookingAdd, BookingAddRequst
from src.services.base import BaseService, DataCheckService


class BookingService(BaseService):
    async def get_all_bookings(self):
        return await self.db.bookings.get_all()

    async def get_user_bookings(self, user_id: int):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def add_booking(self, booking_data: BookingAddRequst, user_id: int):
        room = await DataCheckService.check_room_exists(
            room_id=booking_data.room_id, db=self.db
        )

        price_room: int = room.price  # type: ignore
        _booking_data = BookingAdd(
            user_id=user_id, price=price_room, **booking_data.model_dump()
        )

        try:
            booking = await self.db.bookings.add_booking(
                _booking_data, hotel_id=room.hotel_id
            )
        except NoAvailableRoomsException as ex:
            raise NoAvailableRoomsException from ex

        await self.db.commit()

        return booking
