from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

# ============================================================
# ROUTES
# ============================================================

@api.route('/')
class AmenityList(Resource):
    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    def post(self):
        """Create a new amenity (admin only)"""
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        amenity_data = api.payload
        name = amenity_data.get('name')

        # Guard against duplicate names
        if facade.get_amenity_by_name(name):
            return {'error': 'Amenity with this name already exists'}, 400

        try:
            amenity = facade.create_amenity(amenity_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {'id': amenity.id, 'name': amenity.name}, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [{'id': a.id, 'name': a.name} for a in amenities], 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name}, 200

    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(403, 'Admin privileges required')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity (admin only)"""
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        amenity_data = api.payload
        name = amenity_data.get('name')

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
 
        # Guard against duplicate names from a different amenity
        existing = facade.get_amenity_by_name(name)
        if existing and existing.id != amenity_id:
            return {'error': 'Amenity with this name already exists'}, 400
        
        try:
            updated = facade.update_amenity(amenity_id, amenity_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {'message': 'Amenity updated successfully'}, 200

