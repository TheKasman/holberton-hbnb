from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
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
    'owner_id': fields.String(required=True, description='ID of the owner'),
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

    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new place"""
        try:
            place = facade.create_place(request.json)

            return {
                "id": place.id,
                "title": place.title,
                "description": place.description,
                "price": place.price,
                "latitude": place.latitude,
                "longitude": place.longitude,
                "owner_id": place.owner.id
            }, 201

        except ValueError as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
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
            "owner_id": place.owner.id
        } for place in places], 200

# ============================================================
# Additional routes for place details and reviews
# ============================================================

@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        return [{
            "id": review.id,
            "rating": review.rating,
            "comment": review.comment,
            "reviewer": {
                "id": review.reviewer.id,
                "first_name": review.reviewer.first_name,
                "last_name": review.reviewer.last_name,
                "email": review.reviewer.email
            }
        } for review in place.reviews], 200

@api.route('/<place_id>')
class PlaceResource(Resource):

    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
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
            "owner": {
                "id": place.owner.id,
                "first_name": place.owner.first_name,
                "last_name": place.owner.last_name,
                "email": place.owner.email
            },
            "amenities": [
                {
                    "id": amenity.id,
                    "name": amenity.name
                } for amenity in place.amenities
            ]
        }, 200

    @api.expect(update_place_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    def put(self, place_id):
        try:
            place = facade.update_place(place_id, request.json)
            return {
                "id": place.id,
                "title": place.title,
                "description": place.description,
                "price": place.price,
                "latitude": place.latitude,
                "longitude": place.longitude,
                "owner_id": place.owner.id
            }, 200

        except ValueError as e:
            if str(e) == "Place not found":
                return {"error": str(e)}, 404
            return {"error": str(e)}, 400
        

# -----------------------------------------Admin-----------------------------------------

# allows admins or owners to modify a place
@api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @jwt_required()
    @api.expect(place_model, validate=True)
    @api.response(200, 'Place successfully updated')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    def put(self, place_id):
        current_user = get_jwt()

        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        # retrieves place
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        # if not admin or place owner, PUBLICLY SHAME THEM BOOOOOOOOOOOOOO
        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403
        
        # input data for modification
        data = request.json
        name = data.get('name')
        description = data.get('description')
        city_id = data.get('city_id')

        # checks if you put in all required fields
        if not name or not description:
            return {'error': 'Missing required fields: name or description'}, 400
        
        # newly updated place info
        place.name = name
        place.description = description
        if city_id:
            place.city_id = city_id

        # persist changes
        facade.update_place(place)

        # return newly updated place
        return {
            'id': place.id,
            'name': place.name,
            'description': place.description,
            'city_id': place.city_id,
            'owner_id': place.owner_id
        }, 200