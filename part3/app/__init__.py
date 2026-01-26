# app/__init__.py
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from app.config import Config
from app.models import db  # SQLAlchemy database instance

# Initialize extensions
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class=Config):
    """Factory function to create and configure the Flask app"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)  # Initialize SQLAlchemy with the Flask app

    # Register blueprints
    from app.routes.user_routes import user_bp
    from app.routes.place_routes import place_bp
    from app.routes.review_routes import review_bp
    from app.routes.amenity_routes import amenity_bp  # Admin-only amenities

    app.register_blueprint(user_bp, url_prefix='/users')      # User endpoints
    app.register_blueprint(place_bp, url_prefix='/places')    # Place endpoints
    app.register_blueprint(review_bp, url_prefix='/reviews')  # Review endpoints
    app.register_blueprint(amenity_bp, url_prefix='/amenities')  # Amenity endpoints

    return app
