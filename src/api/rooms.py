from datetime import date
from fastapi import APIRouter, Body, HTTPException

from src.schemas.facilities import RoomFacilityAdd
from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int, db: DBDep, date_from : date, date_to : date):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get("{hotel_id}/rooms/{room_id}", description="Получение номера по ID")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


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
                    "description": 'string',
                    "price": 4500,
                    "quantity": 5,
                    "facilities_ids": None,
                },
            },
            "2": {
                "summary": "Эконом",
                "value": {
                    "title": "Номер на одного",
                    "description": 'string',
                    "price": 1500,
                    "quantity": 7,
                    "facilities_ids": None,
                },
            },
        }
    ),
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    if room_data.facilities_ids:
        rooms_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
        await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {"status": "OK", "data": room}



@router.put("/{hotel_id}/rooms/{room_id}")
async def update_room(
    hotel_id: int, room_id: int, db: DBDep, room_data: RoomAddRequest = Body()
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.edit(_room_data, id=room_id, hotel_id=hotel_id)
    if room_data.facilities_ids:
        rooms_facilities_data = [RoomFacilityAdd(room_id=room_id, facility_id=f_id) for f_id in room_data.facilities_ids]
        await db.rooms_facilities.update_facilities(data=rooms_facilities_data, room_id=room_id)
    await db.commit()
    return {"status": "OK"}
    

@router.patch("/{hotel_id}/rooms/{room_id}")
async def update_patc_room(
    hotel_id: int, room_id: int, room_data: RoomPatchRequest, db: DBDep
):
    _room_data = RoomPatch(
        hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True)
    )
    await db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    if room_data.facilities_ids:
        rooms_facilities_data = [RoomFacilityAdd(room_id=room_id, facility_id=f_id) for f_id in room_data.facilities_ids]
        await db.rooms_facilities.update_facilities(data=rooms_facilities_data, room_id=room_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}
