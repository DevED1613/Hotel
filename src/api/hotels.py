from datetime import date

from fastapi import APIRouter, Body, HTTPException, Query
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, PaginationDep
from src.exceptions import ObjectNotFoundException, check_date_to_after_date_from
from src.schemas.hotels import HotelAdd, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=15)
async def get_hotels(
    pagintation: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Адрес отеля"),
    date_from: date = Query(
        examples=[
            "2024-08-01",
        ],
        description="Дата заезда",
    ),
    date_to: date = Query(
        examples=[
            "2024-08-10",
        ],
        description="Дата выезда",
    ),
):
    check_date_to_after_date_from(date_from=date_from, date_to=date_to)
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        limit=pagintation.per_page,
        offset=(pagintation.page - 1) * pagintation.per_page,
    )


@router.get("/{hotel_id}", description="Получение отеля по ID")
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Отель не найден")


@router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель 5 звезд у моря",
                    "location": "Ул. Пушкина дом Колотушкина",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {"title": "Отель в пустыне", "location": "Ул. Абу-Бандита 5"},
            },
        }
    ),
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def update_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    try:
        await db.hotels.edit(hotel_data, id=hotel_id)

    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Отель не найден")

    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}")
async def update_patch_hotel(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    try:
        await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)

    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Отель не найден")

    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    try:
        await db.hotels.delete(id=hotel_id)

    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Отель не найден")

    await db.commit()
    return {"status": "OK"}
