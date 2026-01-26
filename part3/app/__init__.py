from flask import Flask
from app.config import Config
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Initialize blueprints or other extensions here

    return app
