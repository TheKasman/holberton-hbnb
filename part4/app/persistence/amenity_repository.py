"""Amenity repository"""

from app.models.amenity import Amenity
from app.persistence.repository import SQLAlchemyRepository


class AmenityRepository(SQLAlchemyRepository):
    """Amenity-specific queries"""

    def __init__(self):
        super().__init__(Amenity)