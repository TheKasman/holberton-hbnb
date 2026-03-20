"""User model module"""

import re
from app.models.baseclass import BaseModel
from app.extensions import db, bcrypt


class User(BaseModel):
    __tablename__ = "users"

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    # Email must be unique for login purposes
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)

    # Stores hashed password only (never plain text)
    password = db.Column(db.String(128), nullable=False)

    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    # =========================
    # Relationships
    # =========================
    # One-to-Many: A User can own many Places
    places = db.relationship('Place', backref='owner', lazy=True,
                             cascade='all, delete-orphan')
 
    # One-to-Many: A User can write many Reviews
    reviews = db.relationship('Review', backref='author', lazy=True,
                              cascade='all, delete-orphan')
    
    # =========================
    # Validation Methods
    # =========================

    def set_first_name(self, first_name):
        if not isinstance(first_name, str) or not first_name.strip():
            raise ValueError("first_name must be a non-empty string")

        self.first_name = first_name.strip()

    def set_last_name(self, last_name):
        if not isinstance(last_name, str) or not last_name.strip():
            raise ValueError("last_name must be a non-empty string")

        self.last_name = last_name.strip()

    def set_email(self, email):
        if not isinstance(email, str) or not email.strip():
            raise ValueError("email must be a non-empty string")

        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format")

        self.email = email.strip()

    def set_password(self, password):
        if not isinstance(password, str) or not password.strip():
            raise ValueError("password must be a non-empty string")

        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)