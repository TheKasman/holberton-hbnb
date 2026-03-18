"""Users endpoint module"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description="Password of the user")
})

update_user_model = api.model('UpdateUser', {
    'first_name': fields.String(required=False, description='First name of the user'),
    'last_name': fields.String(required=False, description='Last name of the user'),
})

@api.route('/')
class UserList(Resource):
    """Users API modules"""

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return {'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email
            }, 201

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve list of users"""
        users = facade.user_repo.get_all()

        return [
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
            for user in users
        ], 200


@api.route('/<user_id>')
class UserResource(Resource):
    """Get things from a created user"""

    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }, 200

    @jwt_required()
    @api.expect(update_user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(400, 'Cannot modify email or password')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user details (own account only, no email/password changes)"""
        current_user_id = get_jwt_identity()

        # Users can only modify their own data
        if current_user_id != user_id:
            return {'error': 'Unauthorized action'}, 403
        
        user = facade.get_user(user_id)

        if not user:
            return {'error': 'User not found'}, 404

        data = api.payload

        # Block email or password modification on this endpoint
        if 'email' in data or 'password' in data:
            return {'error': 'You cannot modify email or password'}, 400

        # Update fields
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

