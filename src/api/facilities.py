from fastapi import APIRouter, Body

from src.schemas.facilities import FacilityAdd
from src.api.dependencies import DBDep

router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("")
async def get_all_facilities(db: DBDep):
    return await db.facilities.get_all()

@router.post("")
async def create_facility(
    db: DBDep,
    facility_data: FacilityAdd = Body()
):
    facility =  await db.facilities.add(facility_data)
    await db.commit()

    return {"status": "OK", "data": facility}


@router.delete("/{facility_id}")
async def delete_facility(facility_id: int, db: DBDep):
    await db.facilities.delete(id=facility_id)
    await db.commit()
    return {"status": "OK"}