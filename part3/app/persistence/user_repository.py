"""User repository"""

from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    """User-specific queries"""

    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        """Find user by email"""
        if not email:
            return None
        return self.model.query.filter_by(
            email=email.strip().lower()
        ).first()

    def exists_by_email(self, email):
        """Check if email exists"""
        return self.get_user_by_email(email) is not None

    def get_all_admins(self):
        """Get all admin users"""
        return self.model.query.filter_by(is_admin=True).all()