from pydantic import EmailStr
from sqlalchemy import select

from src.repositories.mappers.mappers import UserDataMapper, UserInDBMapper
from repositories.base import BaseRepository
from src.models.users import UsersOrm


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if not model:
            return None
        return UserInDBMapper(model)


    