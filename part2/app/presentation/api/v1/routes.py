from flask_restx import Namespace, Resource

api_v1 = Namespace("health", description="Health check")

@api_v1.route("/")
class Health(Resource):
    def get(self):
        return {"status": "HBnB API is running"}, 200
