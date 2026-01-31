# app/api/v1/users.py
from flask import request
from flask_restx import Namespace, Resource
from app.business.facade import HBnBFacade
from app.models.user import User

facade = HBnBFacade()

api = Namespace("users", description="User operations")


@api.route("/")
class UsersList(Resource):
    def get(self):
        """Get all users"""
        users = [u for u in facade.get_all() if isinstance(u, User)]

        return [
            {
                "id": u.id,
                "email": u.email,
                "first_name": u.first_name,
                "last_name": u.last_name,
            }
            for u in users
        ], 200

    def post(self):
        """Create a new user"""
        data = request.get_json() or {}

        if not data.get("email"):
            return {"error": "Email is required"}, 400

        user = User(
            email=data["email"],
            password=data.get("password", ""),
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
        )

        created_user = facade.create(user)

        return {
            "id": created_user.id,
            "email": created_user.email,
            "first_name": created_user.first_name,
            "last_name": created_user.last_name,
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
        }, 200

    def put(self, user_id):
        """Update user"""
        data = request.get_json() or {}

        user = facade.get(user_id)
        if not user or not isinstance(user, User):
            return {"error": "User not found"}, 404

        updated_user = facade.update(user_id, data)

        return {
            "id": updated_user.id,
            "email": updated_user.email,
            "first_name": updated_user.first_name,
            "last_name": updated_user.last_name,
        }, 200
