#!/usr/bin/python3
"""Module for class amenity"""
from app.models.base_model import BaseModel
from app.extensions import db


class Amenity(BaseModel):
    """Amenity class blueprint"""

    __tablename__ = "amenities"

    # ==========================
    # Columns Mapping
    # ==========================
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50), nullable=False)

    # ==========================================================
    # NOTE:
    # Relationships will be added later (e.g., Place <-> Amenity)
    # ==========================================================

    # ==========================
    # Validation Methods
    # ==========================

    def set_name(self, name):
        """Validate and set amenity name"""
        if not name or not isinstance(name, str) or len(name) > 50:
            raise ValueError("Amenity name must be a non-empty string of max 50 characters")
        self.name = name

    # ==========================
    # Serialization
    # ==========================

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }