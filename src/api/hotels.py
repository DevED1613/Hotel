from fastapi import Query, Body, APIRouter

from src.schemas.hotels import HotelAdd, HotelPatch
from src.api.dependencies import DBDep, PaginationDep



router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
    pagintation: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Адрес отеля"),
):
    return await db.hotels.get_all(
        location=location,
        title=title,
        limit=pagintation.per_page,
        offset=(pagintation.page - 1) * pagintation.per_page,
    )


@router.get("/{hotel_id}", description="Получение отеля по ID")
async def get_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)


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
    )
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def update_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}")
async def update_patch_hotel(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    await db.hotels.edit(
        hotel_data, exclude_unset=True, id=hotel_id
    )
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}
