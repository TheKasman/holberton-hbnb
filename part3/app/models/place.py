from app.models.baseclass import BaseModel
# from app.models.user import User
# from app.models.review import Review
# from app.models.amenity import Amenity
from app.extensions import db


class Place(BaseModel):
    """
    Place business object defined according to Part 2 requirements.
    """

    __tablename__ = "places"

    # ==========================
    # Columns Mapping
    # ==========================
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    # ==========================================================
    # NOTE:
    # Relationships removed temporarily per project instructions.
    # These will be reintroduced in a later stage using SQLAlchemy
    # relationships and foreign keys.
    # ==========================================================

    # owner = db.relationship("User", backref="places")
    # reviews = db.relationship("Review", backref="place", lazy=True)
    # amenities = db.relationship("Amenity", secondary="place_amenity")

    # ==========================
    # Validation Methods
    # ==========================

    def set_title(self, title):
        # Title Validation (Required, max 100 chars)
        if not title or not isinstance(title, str) or len(title) > 100:
            raise ValueError("Place title must be a non-empty string up to 100 characters")
        self.title = title

    def set_description(self, description):
        self.description = description or ""

    def set_price(self, price):
        # Price Validation (Must be positive)
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Price must be a positive value")
        self.price = price

    def set_latitude(self, latitude):
        # Latitude Validation (Required, -90 to 90)
        if latitude is None or not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0")
        self.latitude = latitude

    def set_longitude(self, longitude):
        # Longitude Validation (Required, -180 to 180)
        if longitude is None or not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0")
        self.longitude = longitude

    # ==========================
    # Update Override
    # ==========================

    def update(self, data):
        if "title" in data:
            self.set_title(data["title"])

        if "price" in data:
            self.set_price(data["price"])

        if "latitude" in data:
            self.set_latitude(data["latitude"])

        if "longitude" in data:
            self.set_longitude(data["longitude"])

        if "description" in data:
            self.set_description(data["description"])

        super().update(data)

    # ==========================================================
    # Relationship Methods (Temporarily Disabled)
    # ==========================================================

    # def add_review(self, review):
    #     """
    #     Add a Review instance to this place.
    #     """
    #     if not isinstance(review, Review):
    #         raise ValueError("review must be a Review instance")
    #
    #     if review not in self.reviews:
    #         self.reviews.append(review)

    # def add_amenity(self, amenity):
    #     """
    #     Add an Amenity instance to this place.
    #     """
    #     if not isinstance(amenity, Amenity):
    #         raise ValueError("amenity must be an Amenity instance")
    #
    #     if amenity not in self.amenities:
    #         self.amenities.append(amenity)