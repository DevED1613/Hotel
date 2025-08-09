from datetime import date

from fastapi import APIRouter, Body, Query
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, PaginationDep
from src.exceptions import HotelNotFoundHTTPException, ObjectNotFoundException
from src.schemas.hotels import HotelAdd, HotelPatch
from src.services.hotels import HotelService

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
    HotelService(db).get_filtered_by_time(
        pagintation=pagintation,
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
    )


@router.get("/{hotel_id}", description="Получение отеля по ID")
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_one(hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


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
    hotel = await HotelService(db).add_hotel(hotel_data)
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def update_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    try:
        await HotelService(db).edit_hotel(hotel_data, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK"}


@router.patch("/{hotel_id}")
async def update_patch_hotel(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    try:
        await HotelService(db).edit_hotel(
            hotel_data, hotel_id=hotel_id, exclude_unset=True
        )
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    try:
        await HotelService(db).delete_hotel(hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK"}
