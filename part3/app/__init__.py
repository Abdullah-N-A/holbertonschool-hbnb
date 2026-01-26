# app/__init__.py
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from app.config import Config
from app.models import db  # تأكد إن عندك db في models.py

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
    db.init_app(app)  # لو انت تستخدم SQLAlchemy

    # Register blueprints
    from app.routes.user_routes import user_bp
    from app.routes.place_routes import place_bp
    from app.routes.review_routes import review_bp

    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(place_bp, url_prefix='/places')
    app.register_blueprint(review_bp, url_prefix='/reviews')

    return app
