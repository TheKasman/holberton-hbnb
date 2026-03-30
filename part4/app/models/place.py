from app.models.baseclass import BaseModel
from app.extensions import db

# ==========================
# Association Table
# ==========================
# Many-to-Many: Place <-> Amenity
place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'),
              primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'),
              primary_key=True)
)

class Place(BaseModel):
    """
    Place business object defined according to Part 2 requirements.
    """

    __tablename__ = "places"

    # ==========================
    # Columns Mapping
    # ==========================
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    # ==========================
    # Foreign Keys
    # ==========================
    # One-to-Many: Many Places belong to one User
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'),
                         nullable=False)
 
    # ==========================
    # Relationships
    # ==========================
    # One-to-Many: A Place can have many Reviews
    reviews = db.relationship('Review', backref='place', lazy=True,
                              cascade='all, delete-orphan')
 
    # Many-to-Many: A Place can have many Amenities
    amenities = db.relationship('Amenity', secondary=place_amenity,
                                lazy='subquery',
                                backref=db.backref('places', lazy=True))

    # ==========================
    # Constructor
    # ==========================
    def __init__(self, title, description="", price=None,
                 latitude=None, longitude=None, owner_id=None):
        super().__init__()

        self.set_title(title)
        self.set_description(description)
        self.set_price(price)
        self.set_latitude(latitude)
        self.set_longitude(longitude)

        if owner_id:
            self.owner_id = owner_id

    # ==========================
    # Validation Methods
    # ==========================

    def set_title(self, title):
        if not title or not isinstance(title, str) or len(title) > 100:
            raise ValueError("Place title must be a non-empty string up to 100 characters")
        self.title = title

    def set_description(self, description):
        self.description = description or ""

    def set_price(self, price):
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Price must be a positive value")
        self.price = price

    def set_latitude(self, latitude):
        if latitude is None or not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0")
        self.latitude = latitude

    def set_longitude(self, longitude):
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

        # Only update timestamps, NOT fields again
        self.save()