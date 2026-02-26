#!/usr/bin/python3
from app.models.base_model import BaseModel

# Define a Review class to represent a review object
class Review(BaseModel):
    def __init__ (self, id, text, rating, place, user, created_at, updated_at):
        """Initialize a Review instance."""
        super().__init__(id, created_at, updated_at)
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    


