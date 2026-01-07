from app.business.models.facade import HBnBFacade
from flask_restx import Namespace, Resource
facade = HBnBFacade()

api_v1 = Namespace("health", description="Health check")
@users_ns.route("/")
class UsersList(Resource):
    def get(self):
        users = facade.get_all()

        result = []
        for user in users:
            user_dict = user.to_dict()
            user_dict.pop("password", None)
            result.append(user_dict)

        return result, 200


users_ns = Namespace(
    "users",
    description="User operations",
    path="/api/v1/users"
)
api.add_namespace(api_v1)
api.add_namespace(users_ns)
