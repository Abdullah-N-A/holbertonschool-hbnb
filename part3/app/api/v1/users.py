# app/api/v1/users.py
# app/api/v1/users.py
from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from app.business.facade import HBnBFacade
from app.models.user import User

facade = HBnBFacade()

api = Namespace("users", description="User operations")


@api.route("/")
class UsersList(Resource):
    def get(self):
        """Get all users (public for now)"""
        users = [u for u in facade.get_all() if isinstance(u, User)]

        return [
            {
                "id": u.id,
                "email": u.email,
                "first_name": u.first_name,
                "last_name": u.last_name,
                "is_admin": getattr(u, "is_admin", False),
            }
            for u in users
        ], 200

    def post(self):
        """Create a new user (public registration for now)"""
        data = request.get_json() or {}

        if not data.get("email"):
            return {"error": "Email is required"}, 400
        if not data.get("password"):
            return {"error": "Password is required"}, 400

        # منع تكرار الإيميل
        existing = User.query.filter_by(email=data["email"]).first()
        if existing:
            return {"error": "Email already registered"}, 400

        user = User(
            email=data["email"],
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
        )
        # ✅ hash password
        user.set_password(data["password"])

        created_user = facade.create(user)

        return {
            "id": created_user.id,
            "email": created_user.email,
            "first_name": created_user.first_name,
            "last_name": created_user.last_name,
            "is_admin": getattr(created_user, "is_admin", False),
        }, 201


@api.route("/<string:user_id>")
class UserDetail(Resource):
    def get(self, user_id):
        """Get user by ID"""
        user = facade.get(user_id)

        if not user or not isinstance(user, User):
            return {"error": "User not found"}, 404

        return {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_admin": getattr(user, "is_admin", False),
        }, 200

    @jwt_required()
    def put(self, user_id):
        """
        Update user (authenticated):
        - user can update ONLY his own first_name/last_name
        - cannot modify email/password here
        - admin rules will come later in admin task
        """
        current_user_id = str(get_jwt_identity())
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)

        # user يسمح له يعدل نفسه فقط (إلا لو admin)
        if not is_admin and current_user_id != str(user_id):
            return {"error": "Unauthorized action"}, 403

        data = request.get_json() or {}

        # ممنوع تعديل email/password هنا
        if "email" in data or "password" in data:
            return {"error": "You cannot modify email or password here"}, 400

        user = facade.get(user_id)
        if not user or not isinstance(user, User):
            return {"error": "User not found"}, 404

        updated_user = facade.update(user_id, data)

        return {
            "id": updated_user.id,
            "email": updated_user.email,
            "first_name": updated_user.first_name,
            "last_name": updated_user.last_name,
            "is_admin": getattr(updated_user, "is_admin", False),
        }, 200
