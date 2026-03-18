from app.models.base_model import BaseModel
from app.models.user import User
from app.models.review import Review
from app.models.amenity import Amenity


class Place(BaseModel):
    """
    Place business object defined according to Part 2 requirements.
    """

    def __init__(self, title, description="", price=None,
                 latitude=None, longitude=None, owner=None):
        super().__init__()

        # ==========================
        # Title Validation (Required, max 100 chars)
        # ==========================
        if not title or not isinstance(title, str) or len(title) > 100:
            raise ValueError("Place title must be a non-empty string up to 100 characters")

        # ==========================
        # Price Validation (Must be positive)
        # ==========================
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Price must be a positive value")

        # ==========================
        # Latitude Validation (Required, -90 to 90)
        # ==========================
        if latitude is None or not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0")

        # ==========================
        # Longitude Validation (Required, -180 to 180)
        # ==========================
        if longitude is None or not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0")

        # ==========================
        # Owner Validation (Required, must be User instance)
        # ==========================
        if not isinstance(owner, User):
            raise ValueError("Owner must be a User instance")

        # ==========================
        # Assign Attributes
        # ==========================
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

        # Relationships
        self.reviews = []
        self.amenities = []

    def update(self, data):
        if "title" in data:
            if not data["title"] or len(data["title"]) > 100:
                raise ValueError("Place title must be a non-empty string up to 100 characters")

        if "price" in data:
            if data["price"] <= 0:
                raise ValueError("Price must be a positive value")

        if "latitude" in data:
            if not (-90.0 <= data["latitude"] <= 90.0):
                raise ValueError("Latitude must be between -90.0 and 90.0")

        if "longitude" in data:
            if not (-180.0 <= data["longitude"] <= 180.0):
                raise ValueError("Longitude must be between -180.0 and 180.0")

        super().update(data)
        
    # ==========================================================
    # Relationship Methods
    # ==========================================================

    def add_review(self, review):
        """
        Add a Review instance to this place.
        """
        if not isinstance(review, Review):
            raise ValueError("review must be a Review instance")

        if review not in self.reviews:
            self.reviews.append(review)

    def add_amenity(self, amenity):
        """
        Add an Amenity instance to this place.
        """
        if not isinstance(amenity, Amenity):
            raise ValueError("amenity must be an Amenity instance")

        if amenity not in self.amenities:
            self.amenities.append(amenity)