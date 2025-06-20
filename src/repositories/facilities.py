
from src.schemas.facilities import Facility
from src.models.facilities import FacilitiesOrm
from src.repositories.base import BaseRepository

class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility
    