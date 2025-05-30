from fastapi import APIRouter, Body

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddRequst


router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("")
async def create_booking(
    room_id: int,
    db: DBDep,
    user: UserIdDep,
    booking_data: BookingAddRequst = Body()
    ):
    user = await db.users.get_one_or_none(id=user)
    price = await db.rooms.get_one_or_none(id=room_id)
    print(user)
    _booking_data = BookingAdd(
        room_id=room_id,
        user_id=user.id,
        price=price.price,
        **booking_data.model_dump()
    )
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}
