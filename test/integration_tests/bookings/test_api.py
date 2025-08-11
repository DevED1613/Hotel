from datetime import date

import pytest
import pytest_asyncio
from httpx import AsyncClient

from src.utils.db_manger import DBManager
from test.conftest import get_db_null_poll


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2025-01-01", "2025-01-15", 200),
        (1, "2025-01-01", "2025-01-15", 200),
        (1, "2025-01-01", "2025-01-15", 200),
        (1, "2025-01-01", "2025-01-15", 200),
        (1, "2025-01-01", "2025-01-15", 200),
        (1, "2025-01-01", "2025-01-15", 409),
        (1, "2025-01-16", "2025-01-18", 200),
    ],
)
async def test_add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    status_code: int,
    db: DBManager,
    authenticated_ac: AsyncClient,
):
    room_id = (await db.rooms.get_all())[0].id
    responce = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )

    assert responce.status_code == status_code
    if status_code == 200:
        res = responce.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert "data" in res


@pytest_asyncio.fixture(scope="module")
async def delete_all_bookings():
    async for _db in get_db_null_poll():
        await _db.bookings.delete()
        await _db.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, me_booking",
    [
        (1, "2025-01-01", "2025-01-15", 1),
        (1, "2025-01-01", "2025-01-15", 2),
        (1, "2025-01-01", "2025-01-15", 3),
    ],
)
async def test_add_and_get_bookings(
    room_id: int,
    date_from: date,
    date_to: date,
    me_booking: int,
    delete_all_bookings,
    authenticated_ac: AsyncClient,
):
    responce_add_booking = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    responce_my_booking = await authenticated_ac.get("/bookings/me")
    assert responce_add_booking.status_code == 200
    assert responce_my_booking.status_code == 200
    assert me_booking == len(responce_my_booking.json())
