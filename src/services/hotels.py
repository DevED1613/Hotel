from datetime import date

from src.exceptions import ObjectAlreadyExistsException
from src.schemas.hotels import HotelAdd, HotelPatch
from src.services.base import BaseService, DataCheckService


class HotelService(BaseService):
    async def get_filtered_by_time(
        self,
        pagintation,
        date_from: date,
        date_to: date,
        location: str | None,
        title: str | None,
    ):
        DataCheckService.check_date_to_after_date_from(
            date_from=date_from, date_to=date_to
        )
        return await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=pagintation.per_page,
            offset=(pagintation.page - 1) * pagintation.per_page,
        )

    async def get_one(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def add_hotel(self, hotel_data: HotelAdd):
        if await self._check_object_exists(
            model_repository=self.db.hotels,
            title=hotel_data.title,
            location=hotel_data.location,
        ):
            raise ObjectAlreadyExistsException
        new_hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return new_hotel

    async def edit_hotel(
        self, hotel_data: HotelAdd, hotel_id: int, exclude_unset: bool = False
    ):
        updated_hotel = await self.db.hotels.edit(
            hotel_data, id=hotel_id, exclude_unset=exclude_unset
        )
        await self.db.commit()
        return updated_hotel

    async def patch_hotel(
        self, hotel_data: HotelPatch, hotel_id: int, exclude_unset: bool = True
    ):
        updated_hotel = await self.db.hotels.patch(
            hotel_data, id=hotel_id, exclude_unset=exclude_unset
        )
        await self.db.commit()
        return updated_hotel

    async def delete_hotel(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()
