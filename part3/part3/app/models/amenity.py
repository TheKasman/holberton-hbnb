#!/usr/bin/python3
from app.models.base_model import BaseModel
"""Module for class amenity"""


class Amenity(BaseModel):
    def __init__(self, name):
        """Initialise an Amenity instance."""
        super().__init__()
        if not name or not isinstance(name, str) or len(name) > 50:
            raise ValueError("Amenity name must be a non-empty string of max 50 characters")
        self.name = name
        
