# app/api/v1/auth.py
from flask_restx import Namespace, Resource, fields
from app.models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


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
@api.route("/me")
class Me(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404

        return {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_admin": user.is_admin,
        }, 200
