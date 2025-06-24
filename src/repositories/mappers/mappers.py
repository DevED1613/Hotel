from src.models.bookings import BookingsOrm
from src.models.facilities import FacilitiesOrm
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.models.users import UsersOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.bookings import Booking
from src.schemas.facilities import Facility, RoomFacility
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room, RoomWithFacilities
from src.schemas.users import User, UserInDB


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel


class RoomWithFacilDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = RoomWithFacilities


class RoomDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Room


class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User

class UserInDBMapper(DataMapper):
    db_model = UsersOrm
    schema = UserInDB

class BookingDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = Booking


class FacilitiesDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = Facility

class RoomFacilityDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = RoomFacility

