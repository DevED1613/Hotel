from fastapi import APIRouter, Body, HTTPException
from fastapi_cache.decorator import cache

from src.exceptions import (
    AlreadyExistsError,
    EmptyValueException,
    ObjectNotFoundException,
)
from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd
from src.services.facilities import FacilityService

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=15)
async def get_all_facilities(db: DBDep):
    facilieties = await FacilityService(db).get_all_facilities()
    return {"data": facilieties}


@router.post("")
async def create_facility(db: DBDep, facility_data: FacilityAdd = Body()):
    try:
        facility = await FacilityService(db).add_facility(facility_data)
    except AlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail=f"Удобство с названием '{facility_data.title}' уже существует",
        )
    except EmptyValueException:
        raise HTTPException(
            status_code=400, detail="Название удобства не может быть пустым"
        )

    return {"status": "OK", "data": facility}


@router.delete("/{facility_id}")
async def delete_facility(facility_id: int, db: DBDep):
    try:
        await FacilityService(db).delete_facility(facility_id=facility_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Удобство не найдено")
    return {"status": "OK"}
