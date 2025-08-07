from pydantic import EmailStr
from sqlalchemy import select

from src.schemas.users import UserInDB
from src.repositories.mappers.mappers import UserDataMapper, UserInDBMapper
from src.repositories.base import BaseRepository
from src.models.users import UsersOrm


class UsersRepository(BaseRepository):
    model: type[UsersOrm] = UsersOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr) -> UserInDB | None:
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if not model:
            return None
        return UserInDBMapper.map_to_domain_entity(model)  # type: ignore
