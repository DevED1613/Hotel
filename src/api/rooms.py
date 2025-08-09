from datetime import date

from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.exceptions import (
    HotelNotFoundException,
    HotelNotFoundHTTPException,
    RoomNotFoundException,
    RoomNotFoundHTTPException,
)
from src.schemas.rooms import RoomAddRequest, RoomPatchRequest
from src.services import RoomService

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int, db: DBDep, date_from: date, date_to: date):
    try:
        return await RoomService(db).get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.get("{hotel_id}/rooms/{room_id}", description="Получение номера по ID")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        return await RoomService(db).get_one_with_facilities(
            room_id=room_id, hotel_id=hotel_id
        )
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.post("/{hotel_id}/rooms")
async def create_room(
    hotel_id: int,
    db: DBDep,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Люкс",
                "value": {
                    "title": "Номер на двоих",
                    "description": "string",
                    "price": 4500,
                    "quantity": 5,
                    "facilities_ids": [1, 2],
                },
            },
            "2": {
                "summary": "Эконом",
                "value": {
                    "title": "Номер на одного",
                    "description": "string",
                    "price": 1500,
                    "quantity": 7,
                    "facilities_ids": None,
                },
            },
        }
    ),
):
    try:
        room = await RoomService(db).add_room(hotel_id=hotel_id, room_data=room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_room(
    hotel_id: int, room_id: int, db: DBDep, room_data: RoomAddRequest = Body()
):
    try:
        await RoomService(db).all_edit_room(
            room_data=room_data, room_id=room_id, hotel_id=hotel_id
        )
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def update_patch_room(
    hotel_id: int, room_id: int, room_data: RoomPatchRequest, db: DBDep
):
    try:
        await RoomService(db).update_patch_room(
            room_data=room_data, room_id=room_id, hotel_id=hotel_id
        )
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await RoomService(db).delete_room(room_id=room_id, hotel_id=hotel_id)
    return {"status": "OK"}
