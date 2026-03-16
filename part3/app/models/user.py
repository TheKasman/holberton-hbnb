"""User class module"""

import re
from app.models.base_model import BaseModel



class User(BaseModel):
    """Constructor"""
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()

        #  Variable Validation
        if not isinstance(first_name, str) or not first_name.strip():
            raise ValueError("first_name must be a non-empty string")

        if not isinstance(last_name, str) or not last_name.strip():
            raise ValueError("last_name must be a non-empty string")

        if not isinstance(email, str) or not email.strip():
            raise ValueError("email bust be a non-empty string")

        #  Email structure validation.
        #  I.e. permits emails with underscores, dots etc.
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format")

        if not isinstance(is_admin, bool):
            raise ValueError("is_admin must be a boolean")

        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.email = email.strip()
        self.is_admin = is_admin

        #  Password hashing and initialisation
        if not isinstance(password, str) or not password.strip():
            raise ValueError("password must be a non-empty string")

        self.hash_password(password.strip())

    def hash_password(self, password):
        """Hashes the password before storing it"""
        from app import bcrypt
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        from app import bcrypt
        return bcrypt.check_password_hash(self.password, password)
