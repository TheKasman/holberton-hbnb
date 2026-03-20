"""The HBNB Facade"""
from app.persistence.repository import SQLAlchemyRepository
from app.persistence.user_repository import UserRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.review_repository import ReviewRepository
from app.persistence.amenity_repository import AmenityRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    """Our HBNB Facade class"""
    def __init__(self):
        """Constructor"""
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    # ==========================================================================
    # USER METHODS
    # ==========================================================================

    def create_user(self, user_data):
        """Method for creating a user"""

        # Check if email already exists
        if self.user_repo.exists_by_email(user_data.get("email")):
            raise ValueError("Email already exists")

        user = User()
        user.set_first_name(user_data.get("first_name"))
        user.set_last_name(user_data.get("last_name"))
        user.set_email(user_data.get("email"))
        user.set_password(user_data.get("password"))

        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Gets the user"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Gets the user's email"""
        return self.user_repo.get_user_by_email(email)
    
    def update_user(self, user):
        """Persists an already-modified user object"""
        self.user_repo.add(user)
        return user

    # ==========================================================================
    # PLACE METHODS
    # ==========================================================================

    def create_place(self, place_data):
        """Create a place"""
        req_fields = ["title", "price", "latitude", "longitude", "owner_id"]
        for field in req_fields:
            if field not in place_data:
                raise ValueError(f"Missing required field: {field}")

        # Validate owner exists (kept for future relationship use)
        owner = self.user_repo.get(place_data["owner_id"])
        if not owner:
            raise ValueError("Owner not found")

        # ==========================
        # Create place using setters
        # ==========================
        place = Place(
            title=place_data["title"],
            description=place_data.get("description", ""),
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner_id=place_data["owner_id"]
        )

       # Attach amenities (many-to-many)
        amenity_ids = place_data.get("amenity_ids", [])

        if not isinstance(amenity_ids, list):
            raise ValueError("amenity_ids must be a list")

        for amenity_id in amenity_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity '{amenity_id}' not found")
            place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Get the place"""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Get ALL the places"""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Updates a place object"""
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")

        self.place_repo.update(place_id, place_data)
        return self.get_place(place_id)

    # ==========================================================================
    # REVIEW METHODS
    # ==========================================================================

    def create_review(self, review_data):
        """Creates a review"""
        required_fields = ['text', 'rating', 'user_id', 'place_id']
        for field in required_fields:
            if field not in review_data:
                raise ValueError(f"Missing required field: {field}")

        if not 1 <= review_data['rating'] <= 5:
            raise ValueError("Rating must be between 1 and 5")

        user = self.get_user(review_data['user_id'])
        if not user:
            raise ValueError("User not found")

        place = self.get_place(review_data['place_id'])
        if not place:
            raise ValueError("Place not found")

        # ==========================
        # Create review using setters
        # ==========================
        review = Review(
            text=review_data["text"],
            rating=review_data["rating"],
            place_id=review_data["place_id"],
            user_id=review_data["user_id"]
        )

        self.review_repo.add(review)

        # ==========================================================
        # NOTE:
        # Relationship temporarily disabled
        # ==========================================================
        # place.add_review(review)

        return review

    def get_review(self, review_id):
        """gets a review by ID from the review repository"""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """gets all reviews from the review repository"""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """filters reviews by place_id and returns the list of reviews for that place"""
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")

        reviews = self.review_repo.get_all()
        return [review for review in reviews if review.place_id == place_id]

    def update_review(self, review_id, review_data):
        """Update a review"""
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found")

        if 'text' in review_data:
            review.set_text(review_data['text'])

        if 'rating' in review_data:
            review.set_rating(review_data['rating'])

        self.review_repo.add(review)
        return review

    def delete_review(self, review_id):
        """Delete a review"""
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found")

        self.review_repo.delete(review_id)
        return True

    def get_review_by_id(self, review_id):
        """Get a review by a particular id"""
        return self.get_review(review_id)

    # ==========================================================================
    # AMENITY METHODS
    # ==========================================================================

    def create_amenity(self, amenity_data):
        amenity = Amenity(name=amenity_data["name"])
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by its ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieve all amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an existing amenity's data."""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None

        if 'name' in amenity_data:
            amenity.set_name(amenity_data['name'])

        self.amenity_repo.add(amenity)
        return amenity
    
    def get_amenity_by_name(self, name):
        """Find an amenity by name"""
        amenities = self.amenity_repo.get_all()
        return next((a for a in amenities if a.name == name), None)