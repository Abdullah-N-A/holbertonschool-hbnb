from flask import Blueprint
from flask_restx import Api

api_v1_bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")

api = Api(
    api_v1_bp,
    title="HBnB API",
    version="1.0",
    description="HBnB API v1",
)

# ✅ Import namespaces and register them
from app.api.v1.places import api as places_ns
from app.api.v1.auth import api as auth_ns

api.add_namespace(places_ns, path="/places")
api.add_namespace(auth_ns, path="/auth")
