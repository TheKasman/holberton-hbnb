from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from .users import user_model
from .amenities import amenity_model
from app.services import facade

api = Namespace('places', description='Place operations')

# ============================================================
# API MODELS (for validation & documentation)
# ============================================================

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(required=False, description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude (-90 to 90)'),
    'longitude': fields.Float(required=True, description='Longitude (-180 to 180)'),
    'amenity_ids': fields.List(
        fields.String,
        required=False,
        description='List of amenity IDs'
    )
})

update_place_model = api.model('UpdatePlace', {
    'title': fields.String(required=False),
    'description': fields.String(required=False),
    'price': fields.Float(required=False),
    'latitude': fields.Float(required=False),
    'longitude': fields.Float(required=False)
})

# ============================================================
# ROUTES
# ============================================================

@api.route('/')
class PlaceList(Resource):

    @jwt_required()
    @api.expect(place_model, validate=True)
    def post(self):
        """Create a new place (authenticated users only)"""
        current_user_id = get_jwt_identity()
        data = dict(api.payload)

        # Force owner_id from JWT
        data['owner_id'] = current_user_id

        try:
            place = facade.create_place(data)

            return {
                "id": place.id,
                "title": place.title,
                "description": place.description,
                "price": place.price,
                "latitude": place.latitude,
                "longitude": place.longitude,
                "owner_id": current_user_id   # ✅ FIXED
            }, 201

        except ValueError as e:
            return {"error": str(e)}, 400

    def get(self):
        """Retrieve all places"""
        places = facade.get_all_places()

        return [{
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner_id": None  # ⚠️ TEMP (no relationship yet)
        } for place in places], 200


# ============================================================
# Reviews by place
# ============================================================

@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):

    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        reviews = facade.get_reviews_by_place(place_id)

        if not reviews:
            return {"error": "No reviews found for this place"}, 404

        return [review.to_dict() for review in reviews], 200


# ============================================================
# Single Place Resource
# ============================================================

@api.route('/<place_id>')
class PlaceResource(Resource):

    def get(self, place_id):
        """Retrieve a place by ID"""
        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,

            # ==================================================
            # NOTE: Relationships disabled temporarily
            # ==================================================

            # "owner": {
            #     "id": place.owner.id,
            #     "first_name": place.owner.first_name,
            #     "last_name": place.owner.last_name,
            #     "email": place.owner.email
            # },

            # "amenities": [
            #     {
            #         "id": amenity.id,
            #         "name": amenity.name
            #     } for amenity in place.amenities
            # ]
        }, 200

    @jwt_required()
    @api.expect(update_place_model, validate=True)
    def put(self, place_id):
        """Update a place (owner only)"""
        current_user_id = get_jwt_identity()
        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        # ==================================================
        # NOTE: Ownership check disabled (no relationship yet)
        # ==================================================
        # if place.owner.id != current_user_id:
        #     return {"error": "Unauthorized action"}, 403

        try:
            place = facade.update_place(place_id, request.json)

            return {
                "id": place.id,
                "title": place.title,
                "description": place.description,
                "price": place.price,
                "latitude": place.latitude,
                "longitude": place.longitude,
                "owner_id": current_user_id
            }, 200

        except ValueError as e:
            return {"error": str(e)}, 400