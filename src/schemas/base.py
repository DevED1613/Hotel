from pydantic import BaseModel, field_validator


class BaseSchema(BaseModel):
    """Базовая схема с валидацией строчных полей"""

    @field_validator("*", mode="before")
    @classmethod
    def check_not_empty(cls, value: str) -> str:
        if value is None:
            return value
        if isinstance(value, str) and (not value.strip()):
            raise ValueError("Поле не может быть пустым")
        return value
