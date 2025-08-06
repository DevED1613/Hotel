import pytest
import pytest_asyncio

from test.conftest import get_db_null_poll


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2025-01-01", "2025-01-15", 200),
        (1, "2025-01-01", "2025-01-15", 200),
        (1, "2025-01-01", "2025-01-15", 200),
        (1, "2025-01-01", "2025-01-15", 200),
        (1, "2025-01-01", "2025-01-15", 200),
        (1, "2025-01-01", "2025-01-15", 500),
        (1, "2025-01-16", "2025-01-18", 200),
    ],
)
async def test_add_booking(
    room_id,
    date_from,
    date_to,
    status_code,
    db,
    authenticated_ac,
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


@pytest_asyncio.fixture(scope="session")
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
    room_id,
    date_from,
    date_to,
    me_booking,
    delete_all_bookings,
    authenticated_ac,
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
