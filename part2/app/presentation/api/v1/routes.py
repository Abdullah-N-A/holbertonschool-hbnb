from flask_restx import Namespace, Resource

api_v1 = Namespace("health", description="Health check")

@api_v1.route("/")
class Health(Resource):
    def get(self):
        return {"status": "HBnB API is running"}, 200

users_ns = Namespace(
    "users",
    description="User operations",
    path="/api/v1/users"
)
@users_ns.route("/")
class UsersList(Resource):
    def get(self):
        return {"message": "Users list endpoint"}, 200
api.add_namespace(api_v1)
api.add_namespace(users_ns)
