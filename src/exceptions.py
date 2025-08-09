from fastapi import HTTPException


class BookingServiceException(Exception):
    detail = "Неопределенная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(BookingServiceException):
    detail = "Объект не найден"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"


class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найден"


class NoAvailableRoomsException(BookingServiceException):
    detail = "Нет свободных номеров"


class UserAlreadyExistsError(BookingServiceException):
    detail = "Пользователь уже зарегистрирован"


class DateIncorrectException(BookingServiceException):
    detail = "Дата заезда больше даты выезда"


class BookingServiceHTTPException(HTTPException):
    status_code = 500
    detail = "Неопределенная ошибка"

    def __init__(
        self,
    ):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(BookingServiceHTTPException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPException(BookingServiceHTTPException):
    status_code = 404
    detail = "Номер не найден"
