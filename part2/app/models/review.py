#!/usr/bin/python3
from app.models.base_model import BaseModel

# defines a Review class to represent a review object
class Review(BaseModel):
    def __init__ (self, id, text, rating, place, user, created_at, updated_at):
        """Initialize a Review instance."""
        super().__init__(id, created_at, updated_at)

        #  Text must be non-empty string
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Text must be a non-empty string")
        self.text = text

        # Rating must be integer 1-5
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        self.rating = rating

        # user and place must be non-empty
        if not user:
            raise ValueError("user_id is required")
        if not place:
            raise ValueError("place_id is required")
        self.place = place
        self.user = user

    # defines one to many relationship with Place and User
    def set_place(self, place):
        """Set the place associated with this review."""
        self.place = place

    def set_user(self, user):
        """Set the user associated with this review."""
        self.user = user
