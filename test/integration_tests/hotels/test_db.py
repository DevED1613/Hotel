from src.schemas.hotels import HotelAdd
from src.utils.db_manger import DBManager
from src.database import async_session_maker


async def test_add_hotel():
    hotel_data = HotelAdd(title="Hotel 5 stars", location="Сочи")
    async with DBManager(session=async_session_maker) as db:
        await db.hotels.add(hotel_data)
        await db.commit()