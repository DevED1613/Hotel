import logging
from src.exceptions import AlreadyExistsError, EmptyValueException, ObjectNotFoundException
from src.schemas.facilities import FacilityAdd
from src.services.base import BaseService
from src.tasks.task import test_task


class FacilityService(BaseService):
    async def get_all_facilities(self):
        return await self.db.facilities.get_all()

    async def add_facility(self, facility_data: FacilityAdd):
        if await self.db.facilities.get_one_or_none(title=facility_data.title):
            raise AlreadyExistsError
        facility = await self.db.facilities.add(facility_data)
        await self.db.commit()

        test_task.delay()  # type: ignore
        return facility

    async def delete_facility(self, facility_id: int):
        try:
            deleted = await self.db.facilities.delete(id=facility_id)
        except ObjectNotFoundException as ex:
            raise ObjectNotFoundException from ex
        await self.db.commit()
