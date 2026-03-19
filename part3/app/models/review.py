#!/usr/bin/python3
"""Module containing the key informatino for the Review object"""
from app.models.baseclass import BaseModel
from app.extensions import db


# defines a Review class to represent a review object
class Review(BaseModel):
    """Review class blueprint"""

    __tablename__ = "reviews"

    # ==========================
    # Columns Mapping
    # ==========================
    id = db.Column(db.Integer, primary_key=True)

    text = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    # Foreign key fields (relationships not yet implemented)
    place_id = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.String(60), nullable=False)

    # ==========================================================
    # NOTE:
    # Relationships will be added later using ForeignKey and ORM
    # ==========================================================

    # ==========================
    # Validation Methods
    # ==========================

    def set_text(self, text):
        """Validate and set review text"""
        if not isinstance(text, str) or not text:
            raise ValueError("Text must be a non-empty string.")
        self.text = text

    def set_rating(self, rating):
        """Validate and set rating"""
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5.")
        self.rating = rating

    def set_place(self, place_id):
        """Set the place associated with this review."""
        if not place_id:
            raise ValueError("Place ID must be provided.")
        self.place_id = place_id

    def set_user(self, user_id):
        """Set the user associated with this review."""
        if not user_id:
            raise ValueError("User ID must be provided.")
        self.user_id = user_id

    # ==========================
    # Serialization
    # ==========================

    def to_dict(self):
        """Converts the review object to a serializable dictionary"""
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place_id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }