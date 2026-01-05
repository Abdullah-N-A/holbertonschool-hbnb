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

    from app.presentation.api.v1.routes import api_v1
    # غير هذا السطر ليكون endpoint النهائي /api/v1/health/
    api.add_namespace(api_v1, path="/api/v1/health")

    return app
