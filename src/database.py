from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, NullPool
from sqlalchemy.orm import DeclarativeBase

from config import settings

engine = create_async_engine(settings.DB_URL)
engine_null_poll = create_async_engine(settings.DB_URL, poolclass=NullPool)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
async_session_maker_null_poll = async_sessionmaker(bind=engine_null_poll, expire_on_commit=False)

session = async_session_maker()


class Base(DeclarativeBase):
    pass    