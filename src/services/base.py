from datetime import date

from src.exceptions import (
    DateIncorrectException,
    HotelNotFoundException,
    ObjectNotFoundException,
    RoomNotFoundException,
)
from src.schemas.rooms import RoomWithFacilities
from src.utils.db_manger import DBManager


class BaseService:
    db: DBManager | None

    def __init__(self, db: DBManager | None = None) -> None:
        self.db = db


class DataCheckService:
    @staticmethod
    def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
        """Проверка даты заезда и выезда"""
        if date_to <= date_from:
            raise DateIncorrectException

    @staticmethod
    async def check_hotel_exists(hotel_id: int, db: DBManager) -> None:
        """Проверка существования отеля"""
        try:
            await db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException as ex:
            raise HotelNotFoundException from ex

    @staticmethod
    async def check_room_exists(
        db: DBManager,
        room_id: int,
        hotel_id: int | None = None,
    ) -> RoomWithFacilities:
        """Проверка существования номера"""
        try:
            if not hotel_id:
                room = await db.rooms.get_one(id=room_id)
                return room
            room = await db.rooms.get_one(id=room_id, hotel_id=hotel_id)
            return room
        except ObjectNotFoundException as ex:
            raise RoomNotFoundException from ex
