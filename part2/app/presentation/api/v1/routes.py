from flask import request
from flask_restx import Namespace, Resource
from app.business.models.facade import HBnBFacade
from app.models.user import User

facade = HBnBFacade()

users_ns = Namespace(
    "users",
    description="User operations",
    path="/api/v1/users"
)

@users_ns.route("/")
class UsersList(Resource):
    def get(self):
        users = facade.get_all()
        result = []
        for user in users:
            user_dict = {
                "id": user.id,
                "email": user.email,
                "name": user.name
            }
            result.append(user_dict)
        return result, 200

    def post(self):
        data = request.get_json()
        new_user = User(
            id=data.get("id"),
            email=data.get("email"),
            name=data.get("name"),
            password=data.get("password")
        )
        created_user = facade.create(new_user)
        user_dict = {
            "id": created_user.id,
            "email": created_user.email,
            "name": created_user.name
        }
        return user_dict, 201

@users_ns.route("/<string:user_id>")
class UserDetail(Resource):
    def get(self, user_id):
        user = facade.get(user_id)
        if not user:
            return {"error": "User not found"}, 404
        user_dict = {
            "id": user.id,
            "email": user.email,
            "name": user.name
        }
        return user_dict, 200

    def put(self, user_id):
        user = facade.get(user_id)
        if not user:
            return {"error": "User not found"}, 404
        data = request.get_json()
        updated_user = facade.update(user_id, data)
        user_dict = {
            "id": updated_user.id,
            "email": updated_user.email,
            "name": updated_user.name
        }
        return user_dict, 200
