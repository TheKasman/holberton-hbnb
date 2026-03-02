from app.persistence.repository import InMemoryRepository
import uuid
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ==========================================================================
    # USER METHODS
    # ==========================================================================
    
    #  Method for creating a user
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user


    #  Gets the user
    def get_user(self, user_id):
        return self.user_repo.get(user_id)
    

    #  Gets the user's email
    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    # ==========================================================================
    # PLACE METHODS
    # ==========================================================================

    def create_place(self, place_data):
        # Ensure required fields
        req_fields = ["title", "price", "latitude", "longitude", "owner_id"]
        for field in req_fields:
            if field not in place_data:
                raise ValueError(f"Missing required field: {field}")

        # Validate owner exists
        owner = self.user_repo.get(place_data["owner_id"])
        if not owner:
            raise ValueError("Owner not found")
        
        # Create place
        place = Place(
            title=place_data["title"],
            description=place_data.get("description", ""),
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner=owner
        )

       # Amenities via amenity_ids
        amenity_ids = place_data.get("amenity_ids", [])

        if not isinstance(amenity_ids, list):
            raise ValueError("amenity_ids must be a list")

        # Validate and attach amenities
        for amenity_id in amenity_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity '{amenity_id}' not found")
            place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")

        self.place_repo.update(place_id, place_data)
        return self.get_place(place_id)


    # ==========================================================================
    # REVIEW METHODS
    # ==========================================================================

    # Placeholder methods for creating a review
    def create_review(self, review_data):
        required_fields = ['text', 'rating', 'user_id', 'place_id']
        for field in required_fields:
            if field not in review_data:
                raise ValueError(f"Missing required field: {field}")
            
        if not 1 <= review_data['rating'] <= 5:
            raise ValueError("Rating must be between 1 and 5")
            
        # check if user exists
        user = self.get_user(review_data['user_id'])
        if not user:
            raise ValueError("User not found")
            
        # check if place exists
        place = self.get_place(review_data['place_id'])
        if not place:
            raise ValueError("Place not found")
            
        review = Review(**review_data)
        self.review_repo.add(review)

        # attached the review to the place object so it's up to date
        place.add_review(review)
        return review

    def get_review(self, review_id):
        # gets a review by ID from the review repository
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        # gets all reviews from the review repository
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        
        # filters reviews by place_id and returns the list of reviews for that place
        reviews = self.review_repo.get_all()
        return [review for review in reviews if review.place_id == place_id]

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found")
        
        # updates the review's text and rating based on the provided review_data
        if 'text' in review_data:
            review.text = review_data['text']

        if 'rating' in review_data:
            if not 1 <= review_data['rating'] <= 5:
                raise ValueError("Rating must be between 1 and 5")
            review.rating = review_data['rating']
        
        self.review_repo.update(review_id, review)
        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found")
        
        # deletes the review from the review repository
        self.review_repo.delete(review_id)
        return True


    # ==========================================================================
    # AMENITY METHODS
    # ==========================================================================
    
    # Create an amenity
    def create_amenity(self, amenity_data):
        """Create a new amenity and store it in the repository."""
        amenity = Amenity(name=amenity_data['name'])
        self.amenity_repo.add(amenity)
        return amenity

    # Retrieve an amenity by ID
    def get_amenity(self, amenity_id):
        """Retrieve an amenity by its ID."""
        return self.amenity_repo.get(amenity_id)

    # Retrieve all amenities
    def get_all_amenities(self):
        """Retrieve all amenities."""
        return self.amenity_repo.get_all()

    # Update an amenity
    def update_amenity(self, amenity_id, amenity_data):
        """Update an existing amenity's data."""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        self.amenity_repo.update(amenity_id, amenity_data)
        return amenity
