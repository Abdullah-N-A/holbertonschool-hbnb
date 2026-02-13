from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from config import config
from app.extensions import db, bcrypt, jwt

def create_app(config_class="development"):
    app = Flask(__name__)
    app.config.from_object(config[config_class])

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    # Create DB tables automatically (development only)
    with app.app_context():
        db.create_all()

    # CORS
    CORS(
        app,
        resources={r"/api/*": {"origins": "*"}},
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    )

    # ✅ Register RESTX API + Namespaces
    api = Api(app, title="HBnB API", version="1.0", doc="/api/docs")
    from app.api.v1.places import api as places_ns
    from app.api.v1.auth import api as auth_ns

    api.add_namespace(places_ns, path="/api/v1/places")
    api.add_namespace(auth_ns, path="/api/v1/auth")

    return app
