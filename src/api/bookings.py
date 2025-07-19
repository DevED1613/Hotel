from fastapi import APIRouter, Body

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddRequst


router = APIRouter(prefix="/bookings", tags=["Бронирования"])

@router.get("")
async def get_all_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me")
async def get_booking(db: DBDep, user: UserIdDep):
    return await db.bookings.get_filtered(user_id=user)

@router.post("")
async def create_booking(
    db: DBDep,
    user: UserIdDep,
    booking_data: BookingAddRequst,
    ):
    user = await db.users.get_one_or_none(id=user)
    price = await db.rooms.get_one_or_none(id=booking_data.room_id)
    _booking_data = BookingAdd(
        user_id=user.id,
        price=price.price,
        **booking_data.model_dump()
    )
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}

