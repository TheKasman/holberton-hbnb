from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from flask import request
from werkzeug.security import generate_password_hash
from app.services import facade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email}, 201
    
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
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200
    
    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user details"""
        user = facade.get_user(user_id)

        if not user:
            return {'error': 'User not found'}, 404

        data = api.payload

        # Update fields
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.email = data['email']

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    
# -----------------------------------------Admin----------------------------------------- 


# Allows for admins to create new user(s)
@api.route('/users/')
class AdminUserCreate(Resource):
    @jwt_required()

    def post(self):
        # checking if current user is admin
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        # input data
        user_data = request.json
        email = user_data.get('email')
        first_name = user_data.get('first_name')
        last_name = user_data.get('last_name')
        password = user_data.get('password')

        # checks if missing any fields
        if not first_name or not last_name or not email or not password:
            return {'error': 'Missing required fields'}, 400

        # see if email already in use
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400
        
        # generating a password
        hashed_password = generate_password_hash(password)

        # newly created user
        new_user = facade.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,
            is_admin=user_data.get('is_admin', False)
        )

        # returns newly created user
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email,
            'is_admin': new_user.is_admin
        }, 201
    

    
# Allows for admins to modify any user
@api.route('/users/<user_id>')
class AdminUserModify(Resource):
    @jwt_required()
    def put(self, user_id):
        # logic is largely the same here for this top section as previous endpoint
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password = data.get('password')

        if not first_name or not last_name or not email or not password:
            return {'error': 'Missing required fields'}, 400
        
        # retrieves user info/if not boom error
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        if email:
            # checks email uniqueness
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400
        
        # updated fields if applicable
        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        # updated password if applicable
        if password:
            user.password = generate_password_hash(password)

        # saves changes via facade (function has been made)
        facade.update_user(user)

        # returns updated user info (yippee!)
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_admin': user.is_admin
        }, 200
