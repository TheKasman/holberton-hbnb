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

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
