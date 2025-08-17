from pydantic import BaseModel, field_validator

from src.exceptions import EmptyValueException


class BaseSchema(BaseModel):
    '''Базовая схема с валидацией строчных полей'''
    @field_validator('*', mode='before')
    @classmethod
    def check_not_empty(cls, value: str) -> str:
        if isinstance(value, str) and (not value or value.strip() == ''):
            raise ValueError
        return value