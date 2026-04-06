from flask import Flask, render_template
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.reviews import api as review_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.auth import api as auth_ns
from flask_jwt_extended import JWTManager
from app.extensions import db, bcrypt



jwt = JWTManager()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    api = Api(app, version='1.0', title='HBnB API',
               description='HBnB Application API', doc='/api/v1/')

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    #  Hard coded webpages for now
    @app.route('/index')
    @app.route('/index.html')
    def index_page():
        return render_template('index.html')

    @app.route('/login')
    @app.route('/login.html')
    def login_page():
        return render_template('login.html')

    @app.route('/place')
    @app.route('/place.html')
    def place_page():
        return render_template('place.html')

    @app.route('/add_review')
    @app.route('/add_review.html')
    def add_review_page():
        return render_template('add_review.html')

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(review_ns, path='/api/v1/reviews')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    return app
