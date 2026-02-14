# app/__init__.py
from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from config import config
from app.extensions import db, bcrypt, jwt


def create_app(config_class="development"):
    app = Flask(__name__)
    app.config.from_object(config[config_class])

    # Extensions
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    # 🔥 مهم جداً: استيراد كل المودلز قبل create_all
    from app.models.user import User
    from app.models.place import Place
    from app.models.review import Review
    from app.models.amenity import Amenity

    # Create DB tables (development only)
    with app.app_context():
        db.create_all()

    # CORS
    CORS(
        app,
        resources={r"/api/*": {"origins": "*"}},
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    )

    # API
    api = Api(app, title="HBnB API", version="1.0", prefix="/api/v1")

    # Register namespaces
    from app.api.v1.places import api as places_ns
    from app.api.v1.auth import api as auth_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.users import api as users_ns

    api.add_namespace(places_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(reviews_ns)
    api.add_namespace(amenities_ns)
    api.add_namespace(users_ns)

    return app
