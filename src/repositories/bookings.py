from sqlalchemy import insert, select

from src.schemas.bookings import Booking
from src.repositories.base import BaseRepository
from src.models.bookings import BookingOrm

class BookingsRepository(BaseRepository):
    model = BookingOrm
    schema = Booking

    