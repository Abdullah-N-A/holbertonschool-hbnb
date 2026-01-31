# app/api/v1/users.py
from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app.business.facade import HBnBFacade
from app.models.user import User

facade = HBnBFacade()
api = Namespace("users", description="User operations")


@api.route("/")
class UsersList(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if not claims.get("is_admin"):
            return {"error": "Forbidden"}, 403

        users = User.query.all()
        return [
            {
                "id": u.id,
                "email": u.email,
                "first_name": u.first_name,
                "last_name": u.last_name,
                "is_admin": u.is_admin,
            }
            for u in users
        ], 200

    def post(self):
        data = request.get_json() or {}

        if not data.get("email") or not data.get("password"):
            return {"error": "Email and password are required"}, 400

        if User.query.filter_by(email=data["email"]).first():
            return {"error": "Email already exists"}, 400

        user = User(
            email=data["email"],
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
        )
        user.set_password(data["password"])

        created = facade.create(user)

        return {
            "id": created.id,
            "email": created.email,
            "first_name": created.first_name,
            "last_name": created.last_name,
        }, 201


@api.route("/<string:user_id>")
class UserDetail(Resource):
    @jwt_required()
    def get(self, user_id):
        claims = get_jwt()
        current_user_id = get_jwt_identity()

        if not claims.get("is_admin") and current_user_id != user_id:
            return {"error": "Forbidden"}, 403

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

    @jwt_required()
    def put(self, user_id):
        claims = get_jwt()
        current_user_id = get_jwt_identity()

        if not claims.get("is_admin") and current_user_id != user_id:
            return {"error": "Forbidden"}, 403

        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404

        data = request.get_json() or {}

        allowed = {"first_name", "last_name"}
        if claims.get("is_admin"):
            allowed.add("is_admin")

        for k, v in data.items():
            if k in allowed:
                setattr(user, k, v)

        if "password" in data and data["password"]:
            if claims.get("is_admin") or current_user_id == user_id:
                user.set_password(data["password"])

        facade.create(user)  # commit (create uses session.add+commit)

        return {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_admin": user.is_admin,
        }, 200
