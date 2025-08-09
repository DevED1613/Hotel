from datetime import date

from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import Room, RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest
from src.services.base import BaseService, DataCheckService


class RoomService(BaseService):
    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):
        DataCheckService.check_date_to_after_date_from(
            date_from=date_from, date_to=date_to
        )
        return await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

    async def get_one_with_facilities(self, room_id: int, hotel_id: int):
        return await self.db.rooms.get_one_with_facilities(
            id=room_id, hotel_id=hotel_id
        )

    async def get_one(self, room_id: int):
        return await self.db.rooms.get_one(id=room_id)

    async def add_room(self, hotel_id: int, room_data: RoomAddRequest):
        await DataCheckService.check_hotel_exists(hotel_id, self.db)

        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        room: Room = await self.db.rooms.add(_room_data)  # type: ignore
        if room_data.facilities_ids:
            rooms_facilities_data = [
                RoomFacilityAdd(room_id=room.id, facility_id=f_id)
                for f_id in room_data.facilities_ids
            ]
            await self.db.rooms_facilities.add_bulk(rooms_facilities_data)
        await self.db.commit()
        return room

    async def edit_room(
        self,
        facilities_ids: list[int] | None,
        room_data: RoomAdd | RoomPatch,
        room_id: int,
        hotel_id: int,
        exclude_unset: bool = False,
    ):
        await DataCheckService.check_hotel_exists(hotel_id, self.db)
        await DataCheckService.check_room_exists(
            db=self.db,
            room_id=room_id,
            hotel_id=hotel_id,
        )
        await self.db.rooms.edit(room_data, id=room_id, exclude_unset=exclude_unset)

        if facilities_ids:
            rooms_facilities_data = [
                RoomFacilityAdd(room_id=room_id, facility_id=f_id)
                for f_id in facilities_ids
            ]

            await self.db.rooms_facilities.update_facilities(
                data=rooms_facilities_data, room_id=room_id
            )
        await self.db.commit()

    async def all_edit_room(
        self, room_data: RoomAddRequest, room_id: int, hotel_id: int
    ):
        facilities_ids: list[int] | None = room_data.facilities_ids
        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())

        await self.edit_room(
            facilities_ids, _room_data, room_id=room_id, hotel_id=hotel_id
        )

    async def update_patch_room(
        self, room_data: RoomPatchRequest, room_id: int, hotel_id: int
    ):
        facilities_ids: list[int] | None = room_data.facilities_ids
        _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump())

        await self.edit_room(
            facilities_ids=facilities_ids,
            room_data=_room_data,
            room_id=room_id,
            hotel_id=hotel_id,
            exclude_unset=True,
        )

    async def delete_room(self, room_id: int, hotel_id: int):
        await DataCheckService.check_room_exists(
            db=self.db,
            room_id=room_id,
            hotel_id=hotel_id,
        )

        await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await self.db.commit()
