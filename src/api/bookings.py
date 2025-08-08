from fastapi import APIRouter, HTTPException

from src.exceptions import NoAvailableRoomsException, ObjectNotFoundException
from src.schemas.hotels import Hotel
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
    user_id: UserIdDep,
    booking_data: BookingAddRequst,
):
    try:
        room = await db.rooms.get_one(id=booking_data.room_id)  # type: ignore
    except ObjectNotFoundException as ex:
        raise HTTPException(status_code=404, detail="Номер не найден")

    try:
        hotel: Hotel = await db.hotels.get_one(id=room.hotel_id)  # type: ignore
    except ObjectNotFoundException as ex:
        raise HTTPException(status_code=404, detail="Отель не найден")

    price_room: int = room.price  # type: ignore
    _booking_data = BookingAdd(
        user_id=user_id, price=price_room, **booking_data.model_dump()
    )

    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    except NoAvailableRoomsException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)

    await db.commit()

    return {"status": "OK", "data": booking}
