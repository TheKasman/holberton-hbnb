import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "supersecretkey" #  TO BE THROWN AWAY SOON POSSIBLY
    JWT_SECRET_KEY = "supersecretjwtkey" #  TO BE THROWN AWAY SOON POSSIBLY
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'development.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}