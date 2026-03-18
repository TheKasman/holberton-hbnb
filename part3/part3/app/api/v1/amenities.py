from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload

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

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity_data = api.payload

        try:
            amenity = facade.update_amenity(amenity_id, amenity_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        if not amenity:
            return {'error': 'Amenity not found'}, 404

        return {'message': 'Amenity updated successfully'}, 200


# -----------------------------------------Admin-----------------------------------------


# allows admin to create new amenities
@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @jwt_required()
    @api.expect(amenity_model, validate=True)
    # Success and error responses
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input or amenity already exists')
    def post(self):
        # checks if current user is admin
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        # input info for new amenities
        data = request.json
        name = data.get('name')

        # needs to have an amenity name (duh)
        if not name:
            return {'error': 'Missing required field: name'}, 400
        
        # checks if amenity has same name
        if facade.get_amenity_by_name(name):
            return {'error': 'Amenity with this name already exists'}, 400
        
        # creates new amenity
        new_amenity = facade.create_amenity(name=name)

        # returns new amenity
        return {
            'id': new_amenity.id,
            'name': new_amenity.name
        }, 201
    

# allows admin to modify existing amenities
@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    # logic here is largely the same as previous class
    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity successfully updated')
    @api.response(400, 'Invalid input or name already exists')
    @api.response(404, 'Amenity not found')
    def put(self, amenity_id):
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        # input data
        data = request.json
        name = data.get('name')

        # needs a name 
        if not name:
            return {'error': 'Missing required field: name'}, 400
        
        # retrieve amenity through facade
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        
        # make sure its not a conflicting amenity
        existing_amenity = facade.get_amenity_by_name(name)
        if existing_amenity and existing_amenity.id != amenity_id:
            return {'error': 'Amenity with this name already exists'}, 400
        
        # newly updated amenity name
        amenity.name = name

        # persist changes to facade
        facade.update_amenity(amenity)

        # returns newly updated amenity
        return {
            'id': amenity.id,
            'name': amenity.name
        }, 200
