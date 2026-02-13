# app/__init__.py
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

    # ✅ CORS (خليها بسيطة وبدون credentials)
    CORS(
        app,
        resources={r"/api/*": {"origins": "*"}},
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    )

    return app