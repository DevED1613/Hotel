import logging

from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import (
    NoAvailableRoomsException,
    RoomNotFoundException,
    RoomNotFoundHTTPException,
)
from src.schemas.bookings import BookingAddRequst
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
async def get_all_bookings(db: DBDep):
    return await BookingService(db).get_all_bookings()


@router.get("/me")
async def get_booking(db: DBDep, user: UserIdDep):
    return await BookingService(db).get_user_bookings(user_id=user)


@router.post("")
async def create_booking(
    db: DBDep,
    user_id: UserIdDep,
    booking_data: BookingAddRequst,
):
    try:
        logging.info(f"Booking data: {booking_data}")
        logging.info(f"User id: {user_id}")
        booking = await BookingService(db).add_booking(booking_data, user_id=user_id)
    except NoAvailableRoomsException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException

    return {"status": "OK", "data": booking}
