"""Place repository"""

from app.models.place import Place
from app.persistence.repository import SQLAlchemyRepository


class PlaceRepository(SQLAlchemyRepository):
    """Place-specific queries"""

    def __init__(self):
        super().__init__(Place)