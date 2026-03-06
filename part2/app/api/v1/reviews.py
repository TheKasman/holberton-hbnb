from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    """Core functionality for review lists."""
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        data = request.json

        # checks if the rating is between 1 and 5
        if not 1 <= data.get('rating', 0) <= 5:
            api.abort(400, 'Rating must be between 1 and 5')

        # returns created review with status code 201 or
        # an error message with status code 400 if the input data is invalid
        try:
            review = facade.create_review(data)
            return review.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))


    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()

        if not reviews:
            api.abort(404, 'No reviews found')

        return [review.to_dict() for review in reviews], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review_by_id(review_id)

        if not review:
            api.abort(404, 'Review not found')

        return review.to_dict(), 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        data = request.json

        # checks if the rating is between 1 and 5
        if not 1 <= data.get('rating', 0) <= 5:
            api.abort(400, 'Rating must be between 1 and 5')

        try:
            updated_review = facade.update_review(review_id, data)
            return updated_review.to_dict(), 200

        except ValueError as e:
            api.abort(400, str(e))
        except KeyError:
            api.abort(404, 'Review not found')

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        deleted = facade.delete_review(review_id)

        if not deleted:
            api.abort(404, 'Review not found')

        return {"message": "Review deleted successfully"}, 200
