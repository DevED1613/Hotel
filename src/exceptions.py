from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError


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


class FacilityNotFoundException(ObjectNotFoundException):
    detail = "Удобства в списке не найдены"


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


class FacilityNotFoundHTTPException(BookingServiceHTTPException):
    status_code = 404
    detail = "Удобства в списке не найдены"


class NoFieldsToUpdateHTTPException(BookingServiceHTTPException):
    status_code = 400
    detail = "Нет полей для обновления"


class DateIncorrectHTTPException(BookingServiceHTTPException):
    status_code = 400
    detail = "Дата заезда не может быть больше даты выезда"


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    formatted_errors = []

    for err in exc.errors():
        field = ".".join(str(loc) for loc in err.get("loc", []) if loc not in ("body",))
        msg = err.get("msg")
        err_type = err.get("type")

        if err_type == "missing":
            msg = "Обязательное поле отсутствует"
        elif err_type == "string_type":
            msg = "Поле должно быть строкой"
        elif err_type == "greater_than":
            msg = f"Поле '{field}' должно быть больше 0"
        elif err_type == "string_pattern_mismatch":
            msg = "Поле не может быть пустым или состоять только из пробелов"

        formatted_errors.append({"field": field, "message": msg})

    return JSONResponse(
        status_code=422,
        content={"status": "error", "errors": formatted_errors},
    )


async def validation_exception_handler(
    request: Request, exc: ValidationError | RequestValidationError
):  # noqa F811
    formatted_errors = []

    for err in exc.errors():
        field = ".".join(str(loc) for loc in err.get("loc", []) if loc not in ("body",))
        msg = err.get("msg")
        err_type = err.get("type")

        if err_type == "missing":
            msg = "Обязательное поле отсутствует"
        elif err_type == "string_type":
            msg = "Поле должно быть строкой"
        elif err_type == "greater_than":
            msg = f"Поле '{field}' должно быть больше 0"
        elif "Поле не может быть пустым" in msg:
            msg = "Поле не может быть пустым или состоять только из пробелов"

        formatted_errors.append({"field": field, "message": msg})

    return JSONResponse(
        status_code=422,
        content={"status": "error", "errors": formatted_errors},
    )
