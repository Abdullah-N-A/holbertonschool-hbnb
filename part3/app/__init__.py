from flask import Flask
from app.config import Config
from flask_bcrypt import Bcrypt

# Initialize bcrypt
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize bcrypt with the app
    bcrypt.init_app(app)

    # Here you can initialize blueprints or other extensions

    return app
