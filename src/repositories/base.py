from typing import Any, Sequence

from asyncpg import UniqueViolationError
from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Base
from src.exceptions import NoFieldsToUpdateException, ObjectNotFoundException
from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model: type[Base]
    mapper: type[DataMapper]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_filtered(self, *filter, **filter_by) -> list:
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(model) for model in result.scalars().all()
        ]

    async def get_all(self, *args, **kwargs) -> list:
        return await self.get_filtered(*args, **kwargs)

    async def get_one_or_none(self, **filter_by: Any) -> BaseModel | None:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def get_one(self, **filter_by: Any) -> BaseModel:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)

        try:
            model = result.scalar_one()
        except NoResultFound as ex:
            raise ObjectNotFoundException from ex
        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel) -> BaseModel:
        try:
            add_data_stmt = (
                insert(self.model).values(**data.model_dump()).returning(self.model)
            )
            result = await self.session.execute(add_data_stmt)
            model = result.scalars().one()
            return self.mapper.map_to_domain_entity(model)
        except IntegrityError as ex:
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise ObjectNotFoundException from ex
            else:
                raise ex

    async def add_bulk(self, data: Sequence[BaseModel]) -> None:
        add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_data_stmt)

    async def edit(
        self,
        data: BaseModel,
        exclude_unset: bool = False,
        **filter_by,  # type: ignore
    ) -> BaseModel:
        update_data_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .returning(self.model)
        )
        result_update = await self.session.execute(update_data_stmt)
        updated_model = result_update.scalars().one_or_none()
        if not updated_model:
            raise ObjectNotFoundException(f"Объект с фильтром {filter_by} не найден")
        return self.mapper.map_to_domain_entity(updated_model)

    async def patch(
        self,
        data: BaseModel,
        exclude_unset: bool = True,
        **filter_by: Any,
    ) -> BaseModel:
        if not data.model_dump(exclude_unset=True):
            raise NoFieldsToUpdateException
        return await self.edit(data, exclude_unset, **filter_by)

    async def delete(self, **filter_by: Any) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by).returning(self.model.id)
        result = await self.session.execute(delete_stmt)
        if not result.scalars().first():
            raise ObjectNotFoundException(f"Объект с фильтром {filter_by} не найден")
