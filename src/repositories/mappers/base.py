from typing import TypeVar

from pydantic import BaseModel

from src.database import Base

DBModelType = TypeVar("DBModelType", bound="Base")
SchemaType = TypeVar("SchemaType", bound="BaseModel")



class DataMapper:
    model: type[DBModelType] = None
    schema: type[SchemaType] = None

    @classmethod
    def map_to_domain_entity(cls, data):
        return cls.schema.model_validate(data, from_attributes=True)
    
    @classmethod
    def map_to_persistence_entity(cls, data):
        return cls.model(**data.model_dump())
    
