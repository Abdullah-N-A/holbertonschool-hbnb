from flask import Flask
from flask_restx import Api

def create_app():
    app = Flask(__name__)

    api = Api(
        app,
        title="HBnB API",
        version="1.0",
        description="HBnB Application API"
    )

    # Users namespace
    from app.api.v1.users import users_ns
    api.add_namespace(users_ns, path="/api/v1/users")

    # Amenities namespace
    from app.api.v1.amenities import api as amenities_ns
    api.add_namespace(amenities_ns, path="/api/v1/amenities")

    return app
