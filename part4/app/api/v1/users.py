from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app.services import facade

api = Namespace('users', description='User operations')

# ============================================================
# API MODELS
# ============================================================
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'is_admin': fields.Boolean(required=False, description='Admin flag', default=False)
})

update_user_model = api.model('UpdateUser', {
    'first_name': fields.String(required=False, description='First name of the user'),
    'last_name': fields.String(required=False, description='Last name of the user'),
    'email': fields.String(required=False, description='Email of the user'),
    'password': fields.String(required=False, description='Password of the user'),
})

# ============================================================
# ROUTES
# ============================================================

@api.route('/')
class UserList(Resource):
    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered or invalid input')
    @api.response(403, 'Admin privileges required')
    def post(self):
        """Create a new user (admin only)"""
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        user_data = api.payload

        if facade.get_user_by_email(user_data['email']):
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email,
            'is_admin': new_user.is_admin
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
    @api.response(400, 'Invalid input')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Modify a user's details. Admins can update any user including email/password.
        Regular users can only update their own first_name and last_name."""
        current_user = get_jwt()
        is_admin = current_user.get('is_admin', False)
        current_user_id = get_jwt_identity()

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        data = dict(api.payload)

        if is_admin:
            # Admins can modify any user's details including email and password
            if 'email' in data:
                existing = facade.get_user_by_email(data['email'])
                if existing and existing.id != user_id:
                    return {'error': 'Email already in use'}, 400
                user.set_email(data['email'])


            if 'first_name' in data:
                user.set_first_name(data['first_name'])
            if 'last_name' in data:
                user.set_last_name(data['last_name'])
            if 'password' in data:
                user.set_password(data['password'])

        else:
            # Regular users can only edit their own profile
            if current_user_id != user_id:
                return {'error': 'Unauthorized action'}, 403
 
            # Email and password changes are not permitted
            if 'email' in data or 'password' in data:
                return {'error': 'You cannot modify email or password'}, 400
 
            if 'first_name' in data:
                user.set_first_name(data['first_name'])
            if 'last_name' in data:
                user.set_last_name(data['last_name'])
 
        facade.update_user(user)
 
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_admin': user.is_admin
        }, 200

