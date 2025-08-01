import json
from pathlib import Path
import pytest

from httpx import AsyncClient, ASGITransport
import pytest_asyncio

from src.config import settings
from src.database import Base, engine_null_pool
from src.models import *
from src.main import app

BASE_DIR = Path(__file__).parent


@pytest_asyncio.fixture(scope="session")
async def async_client():
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
async def add_hotels_and_rooms_in_DB(setup_database, async_client: AsyncClient):
    with open(BASE_DIR / "unit_tests/mock_hotels.json", "r") as f:
        hotels = json.load(f)
    with open(BASE_DIR / "unit_tests/mock_rooms.json", "r") as f:
        rooms = json.load(f)

    for hotel in hotels:
        response = await async_client.post("/hotels", json=hotel)
        assert response.status_code == 200, f"Failed to add hotel: {response.text}"

    for room in rooms:
       hotel_id = room["hotel_id"] 
       response = await async_client.post(f"/hotels/{hotel_id}/rooms", json=room)
       assert response.status_code == 200, f"Failed to add room: {response.text}"

    