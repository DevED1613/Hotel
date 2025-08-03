from fastapi import APIRouter, Body, HTTPException

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
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    price = await db.rooms.get_one_or_none(id=booking_data.room_id)
    if price is None:
        raise HTTPException(status_code=404, detail="Room not found")
    _booking_data = BookingAdd(
        user_id=user.id,
        price=price.price,
        **booking_data.model_dump()
    )
    booking = await db.bookings.add_booking(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}

