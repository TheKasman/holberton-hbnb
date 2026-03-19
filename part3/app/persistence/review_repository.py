"""Review repository"""

from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository


class ReviewRepository(SQLAlchemyRepository):
    """Review-specific queries"""

    def __init__(self):
        super().__init__(Review)