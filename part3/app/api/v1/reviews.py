from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('reviews', description='Review operations')

# ============================================================
# API MODELS
# ============================================================

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

update_review_model = api.model('UpdateReview', {
    'text': fields.String(required=False, description='Text of the review'),
    'rating': fields.Integer(required=False, description='Rating of the place (1-5)')
})

# ============================================================
# ROUTES
# ============================================================

@api.route('/')
class ReviewList(Resource):
    """Core functionality for review lists."""

    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Place not found')
    def post(self):
        """Create a new review (authenticated users only)"""
        current_user_id = get_jwt_identity()
        data = dict(api.payload)

        # Validate rating
        if not 1 <= data.get('rating', 0) <= 5:
            return {'error': 'Rating must be between 1 and 5'}, 400

        # Validate place exists
        place = facade.get_place(data.get('place_id'))
        if not place:
            return {'error': 'Place not found'}, 404

        # Users cannot review their own place
        if place.owner.id == current_user_id:
            return {"error": "You cannot review your own place"}, 400

        # Prevent duplicate review per user per place
        existing_reviews = facade.get_reviews_by_place(data.get('place_id'))
        for review in existing_reviews:
            if review.user_id == current_user_id:
                return {'error': 'You have already reviewed this place'}, 400

        # Force user_id from JWT
        data['user_id'] = current_user_id

        try:
            review = facade.create_review(data)
            return review.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')

    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review_by_id(review_id)

        if not review:
            return {'error': 'Review not found'}, 404

        return review.to_dict(), 200

    @jwt_required()
    @api.expect(update_review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review (author only)"""
        current_user_id = get_jwt_identity()
        is_admin = get_jwt().get('is_admin', False)

        review = facade.get_review_by_id(review_id)

        if not review:
            return {'error': 'Review not found'}, 404

        # Admins bypass authorship check; regular users must own the review
        if not is_admin and review.user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        data = request.json

        # Validate rating ONLY if provided
        if 'rating' in data and not 1 <= data['rating'] <= 5:
            return {'error': 'Rating must be between 1 and 5'}, 400

        try:
            updated_review = facade.update_review(review_id, data)
            return updated_review.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review (author only)"""
        current_user_id = get_jwt_identity()
        is_admin = get_jwt().get('is_admin', False)

        review = facade.get_review_by_id(review_id)

        if not review:
            return {'error': 'Review not found'}, 404

        # Admins bypass authorship check; regular users must own the review
        if not is_admin and review.user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        deleted = facade.delete_review(review_id)

        if not deleted:
            return {'error': 'Review not found'}, 404

        return {"message": "Review deleted successfully"}, 200