from datetime import date
from fastapi import HTTPException


class BookingServiceException(Exception):
    detail = "Неопределенная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(BookingServiceException):
    detail = "Объект не найден"


class HotelNotFoundException(BookingServiceException):
    detail = "Отель не найден"


class RoomNotFoundException(BookingServiceException):
    detail = "Номер не найден"


class NoAvailableRoomsException(BookingServiceException):
    detail = "Нет свободных номеров"


class UserAlreadyExistsError(BookingServiceException):
    detail = "Пользователь уже зарегистрирован"


class DateIncorrectException(BookingServiceException):
    detail = "Дата заезда больше даты выезда"


class BookingServiceHTTPException(HTTPException):
    status_code = 400
    detail = "Неопределенная ошибка"

    def __init__(self, status_code=status_code, detail=detail):
        super().__init__(status_code=status_code, detail=detail)


class HotelNotFoundHTTPException(BookingServiceHTTPException):
    status_code = 404
    detail = "Отель не найден"

class RoomNotFoundHTTPException(BookingServiceHTTPException):
    status_code = 404
    detail = "Номер не найден"


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(status_code=422, detail="Дата заезда не может быть позже даты выезда")