from app.models.base_model import BaseModel
from app.models.user import User
from app.models.review import Review
from app.models.amenity import Amenity


class Place(BaseModel):
    """Place business object defined according to Part 2 requirements """

    def __init__(self, title, description="", price=0.0,
                 latitude=None, longitude=None, owner=None):
        super().__init__()

        # Required fields validation
        if not title or not isinstance(title, str) or len(title) > 100:
            raise ValueError("Place title must be a non-empty string up to 100 characters")
        if price < 0:
            raise ValueError("Price must be a positive float")

        # Coordinates validation
        if latitude is not None and not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0")
        if longitude is not None and not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0")

        # Owner validation
        if owner is not None and not isinstance(owner, User):
            raise ValueError("Owner must be a User instance")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

        # Relationships
        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        """Add a Review instance to this place."""
        if not isinstance(review, Review):
            raise ValueError("review must be a Review instance")
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an Amenity instance to this place."""
        if not isinstance(amenity, Amenity):
            raise ValueError("amenity must be an Amenity instance")
        self.amenities.append(amenity)
