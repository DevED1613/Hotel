import json
from pathlib import Path
import pytest

from httpx import AsyncClient, ASGITransport
import pytest_asyncio

from src.api.dependencies import get_db
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manger import DBManager
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_poll
from src.models import *
from src.main import app

BASE_DIR = Path(__file__).resolve().parent

async def get_db_null_poll():
    async with DBManager(session=async_session_maker_null_poll) as session:
        yield session


@pytest.fixture(scope="function")
async def db() -> DBManager:  # type: ignore
    async for session in get_db_null_poll():
        yield session


app.dependency_overrides[get_db] = get_db_null_poll


@pytest_asyncio.fixture(scope="session")
async def async_client() -> AsyncClient:  # type: ignore
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database, async_client: AsyncClient):
    response = await async_client.post(
        "auth/register", json={"email": "huyamba@123.com", "password": "1613"}
    )
    assert response.status_code == 200, f"Failed to register user: {response.text}"


@pytest.fixture(scope="session", autouse=True)
async def add_hotels_and_rooms_in_DB(setup_database):
    with open(BASE_DIR / "mock_hotels.json", encoding="utf-8") as f:
        hotels = json.load(f)
    with open(BASE_DIR / "mock_rooms.json", encoding="utf-8") as f:
        rooms = json.load(f)

    hotels = [HotelAdd.model_validate(hotel) for hotel in hotels]
    rooms = [RoomAdd.model_validate(room) for room in rooms]

    async with DBManager(session=async_session_maker_null_poll) as db_:
        await db_.hotels.add_bulk(hotels)
        await db_.rooms.add_bulk(rooms)
        await db_.commit()
