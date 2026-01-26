from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from app.config import Config

# Initialize extensions
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with app
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Import routes
    from app import routes

    # Register blueprints if any (optional)
    # app.register_blueprint(routes.bp)

    return app
