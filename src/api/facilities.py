from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd
from src.services.facilities import FacilityService
from src.tasks.task import test_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=15)
async def get_all_facilities(db: DBDep):
    return await FacilityService(db).get_all_facilities()


@router.post("")
async def create_facility(db: DBDep, facility_data: FacilityAdd = Body()):
    facility = await FacilityService(db).add_facility(facility_data)
    test_task.delay()
    return {"status": "OK", "data": facility}


@router.delete("/{facility_id}")
async def delete_facility(facility_id: int, db: DBDep):
    await FacilityService(db).delete_facility(facility_id=facility_id)
    return {"status": "OK"}
