# app/api/v1/auth.py
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.models.user import User

api = Namespace("auth", description="Authentication operations")

login_model = api.model("Login", {
    "email": fields.String(required=True, description="User email"),
    "password": fields.String(required=True, description="User password"),
})

@api.route("/login")
class Login(Resource):
    @api.expect(login_model, validate=True)
    def post(self):
        data = api.payload or {}

        user = User.query.filter_by(email=data["email"]).first()
        if not user or not user.check_password(data["password"]):
            return {"error": "Invalid credentials"}, 401

        # identity = user.id ، ونضيف claim is_admin
        token = create_access_token(
            identity=user.id,
            additional_claims={"is_admin": user.is_admin}
        )
        return {"access_token": token}, 200
