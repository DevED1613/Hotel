from datetime import date
from src.schemas.bookings import BookingAdd


async def test_add_booking(db):
    room_id = (await db.rooms.get_all())[0].id
    user_id = (await db.users.get_all())[0].id
    booking_data = BookingAdd(
        room_id=room_id,
        user_id=user_id,
        date_from=date(year=2025, month=1, day=1),
        date_to=date(year=2025, month=1, day=15), 
        price=100
    )
    await db.bookings.add(booking_data)
    await db.commit()
