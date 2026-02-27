from app.persistence.repository import InMemoryRepository
import uuid

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Placeholder method for creating a user
    def create_user(self, user_data):
        # Logic will be implemented in later tasks
        pass

    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        # Logic will be implemented in later tasks
        pass


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
            
            review = { 
                "id": str(uuid.uuid4()),
                "text": review_data['text'],
                "rating": review_data['rating'],
                "user_id": review_data['user_id'],
                "place_id": review_data['place_id']
            }
            self.review_repo.add(review)
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
        return [review for review in reviews if review['place_id'] == place_id]

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found")
        
        # updates the review's text and rating based on the provided review_data
        if 'text' in review_data:
            review['text'] = review_data['text']

        if 'rating' in review_data:
            if not 1 <= review_data['rating'] <= 5:
                raise ValueError("Rating must be between 1 and 5")
            review['rating'] = review_data['rating']
        
        self.review_repo.update(review_id, review)
        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found")
        
        # deletes the review from the review repository
        self.review_repo.delete(review_id)
        return True