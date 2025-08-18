from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError


class BookingServiceException(Exception):
    detail = "Неопределенная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(BookingServiceException):
    detail = "Объект не найден"

class ObjectAlreadyExistsException(BookingServiceException):
    detail = "Объект уже существует"


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


class EmptyValueException(BookingServiceException):
    detail = "Поле не может быть пустым"


class AlreadyExistsError(BookingServiceException):
    detail = "Объект уже существует"

class NoFieldsToUpdateException(BookingServiceException):
    detail = "Нет полей для обновления"


class BookingServiceHTTPException(HTTPException):
    status_code = 500
    detail = "Неопределенная ошибка"

    def __init__(
        self,
    ):
        super().__init__(status_code=self.status_code, detail=self.detail)


class EmptyValueExceptionHTTPException(BookingServiceHTTPException):
    status_code = 422
    detail = "Поле не может быть пустым или состоять только из пробелов"


class HotelNotFoundHTTPException(BookingServiceHTTPException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPException(BookingServiceHTTPException):
    status_code = 404
    detail = "Номер не найден"

class NoFieldsToUpdateHTTPException(BookingServiceHTTPException):
    status_code = 400
    detail = "Нет полей для обновления"


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    if any("Поле не может быть пустым" in (err.get("msg") or "") for err in errors):
        raise EmptyValueExceptionHTTPException()
    raise exc