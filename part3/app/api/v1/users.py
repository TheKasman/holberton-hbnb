from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from flask import request
from werkzeug.security import generate_password_hash
from app.services import facade

api = Namespace('users', description='User operations')

# ============================================================
# API MODELS
# ============================================================
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

update_user_model = api.model('UpdateUser', {
    'first_name': fields.String(required=False, description='First name of the user'),
    'last_name': fields.String(required=False, description='Last name of the user'),
})

# ============================================================
# ROUTES
# ============================================================

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

        try:
            new_user = facade.create_user(user_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {
            'id': new_user.id,
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
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200
    
    @jwt_required()
    @api.expect(update_user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update own user details (authenticated, no email/password changes)"""
        current_user_id = get_jwt_identity()

        # Users may only modify their own account
        if user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403
        
        data = dict(api.payload)

        # Block email and password modification via this endpoint
        if 'email' in data or 'password' in data:
            return {'error': 'You cannot modify email or password'}, 400

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404


        if 'first_name' in data:
            user.set_first_name(data['first_name'])
        if 'last_name' in data:
            user.set_last_name(data['last_name'])
 
        facade.update_user(user)
 
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

        # newly created user
        try:
            new_user = facade.create_user({
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'password': password,
                'is_admin': user_data.get('is_admin', False)
            })
        except ValueError as e:
            return {'error': str(e)}, 400

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
        user.set_first_name(first_name)
        user.set_last_name(last_name)
        user.set_email(email)
        user.set_password(password)

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
