from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd
from src.tasks.task import test_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=15)
async def get_all_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("")
async def create_facility(db: DBDep, facility_data: FacilityAdd = Body()):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    test_task.delay()

    return {"status": "OK", "data": facility}


@router.delete("/{facility_id}")
async def delete_facility(facility_id: int, db: DBDep):
    await db.facilities.delete(id=facility_id)
    await db.commit()
    return {"status": "OK"}
