from datetime import date
from src.schemas.bookings import BookingAdd


async def test_add_booking_crud(db):
    room_id = (await db.rooms.get_all())[0].id
    user_id = (await db.users.get_all())[0].id
    booking_data = BookingAdd(
        room_id=room_id,
        user_id=user_id,
        date_from=date(year=2025, month=1, day=1),
        date_to=date(year=2025, month=1, day=15),
        price=100,
    )
    await db.bookings.add(booking_data)

    booking = (await db.bookings.get_all())[0]
    booking_get_one = await db.bookings.get_one_or_none(room_id=room_id)

    assert booking == booking_get_one
    assert booking.room_id == room_id
    assert booking.date_from == date(year=2025, month=1, day=1)

    booking_id = (await db.bookings.get_all())[0].id

    booking_data = BookingAdd(
        room_id=room_id,
        user_id=user_id,
        date_from=date(year=2024, month=1, day=10),
        date_to=date(year=2025, month=1, day=15),
        price=10000,
    )
    await db.bookings.edit(data=booking_data, id=booking_id)
    booking = (await db.bookings.get_all())[0]

    assert booking.date_from == date(year=2024, month=1, day=10)
    assert booking.price == 10000

    await db.bookings.delete(id=booking_id)
    assert (await db.bookings.get_all()) == []

    await db.rollback()
