#!/usr/bin/python3
from app.models.base_model import BaseModel

# defines a Review class to represent a review object
class Review(BaseModel):
    def __init__ (self, id, text, rating, place_id, user_id, created_at, updated_at):
        """Initialize a Review instance."""
        super().__init__(id, created_at, updated_at)
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

        # Validate text and rating
        if not isinstance(self.text, str) or not self.text:
            raise ValueError("Text must be a non-empty string.")
        
        # Validate rating is an integer between 1 and 5
        if not isinstance(self.rating, int) or not (1 <= self.rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5.")
        
        # Validate that user_id and place_id are provided
        if not user_id:
            raise ValueError("User ID must be provided.")
        if not place_id:
            raise ValueError("Place ID must be provided.")

    # defines one to many relationship with Place and User
    def set_place(self, place_id):
        """Set the place associated with this review."""
        self.place_id = place_id

    def set_user(self, user_id):
        """Set the user associated with this review."""
        self.user_id = user_id
