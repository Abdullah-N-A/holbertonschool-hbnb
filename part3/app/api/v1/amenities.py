#app/api/v1/amenities.py
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.business.facade import HBnBFacade
from app.models.amenity import Amenity

facade = HBnBFacade()

api = Namespace("amenities", description="Amenity operations")

amenity_model = api.model(
    "Amenity",
    {
        "name": fields.String(required=True, description="Name of the amenity"),
        "description": fields.String(required=False, description="Description of the amenity"),
    },
)


def _admin_only():
    claims = get_jwt()
    return bool(claims.get("is_admin"))


@api.route("/")
class AmenityList(Resource):
    @api.response(200, "List of amenities retrieved successfully")
    def get(self):
        amenities = [a for a in facade.get_all() if isinstance(a, Amenity)]
        return [
            {
                "id": a.id,
                "name": a.name,
                "description": getattr(a, "description", None),
                "created_at": a.created_at.isoformat() if a.created_at else None,
                "updated_at": a.updated_at.isoformat() if a.updated_at else None,
            }
            for a in amenities
        ], 200

    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.response(201, "Amenity successfully created")
    @api.response(400, "Invalid input data")
    @api.response(403, "Admin only")
    def post(self):
        if not _admin_only():
            return {"error": "Admin only"}, 403

        data = api.payload or {}
        name = data.get("name")
        if not name:
            return {"error": "Amenity name is required"}, 400

        new_amenity = Amenity(name=name)
        if "description" in data:
            new_amenity.description = data["description"]

        created = facade.create(new_amenity)

        return {
            "id": created.id,
            "name": created.name,
            "description": getattr(created, "description", None),
            "created_at": created.created_at.isoformat() if created.created_at else None,
            "updated_at": created.updated_at.isoformat() if created.updated_at else None,
        }, 201


@api.route("/<string:amenity_id>")
class AmenityResource(Resource):
    @api.response(200, "Amenity details retrieved successfully")
    @api.response(404, "Amenity not found")
    def get(self, amenity_id):
        a = facade.get(amenity_id)
        if not a or not isinstance(a, Amenity):
            return {"error": "Amenity not found"}, 404

        return {
            "id": a.id,
            "name": a.name,
            "description": getattr(a, "description", None),
            "created_at": a.created_at.isoformat() if a.created_at else None,
            "updated_at": a.updated_at.isoformat() if a.updated_at else None,
        }, 200

    @jwt_required()
    @api.expect(amenity_model)
    @api.response(200, "Amenity updated successfully")
    @api.response(404, "Amenity not found")
    @api.response(403, "Admin only")
    def put(self, amenity_id):
        if not _admin_only():
            return {"error": "Admin only"}, 403

        a = facade.get(amenity_id)
        if not a or not isinstance(a, Amenity):
            return {"error": "Amenity not found"}, 404

        data = api.payload or {}
        updated = facade.update(amenity_id, data)

        return {
            "id": updated.id,
            "name": updated.name,
            "description": getattr(updated, "description", None),
            "created_at": updated.created_at.isoformat() if updated.created_at else None,
            "updated_at": updated.updated_at.isoformat() if updated.updated_at else None,
        }, 200

    @jwt_required()
    @api.response(204, "Amenity deleted successfully")
    @api.response(404, "Amenity not found")
    @api.response(403, "Admin only")
    def delete(self, amenity_id):
        if not _admin_only():
            return {"error": "Admin only"}, 403

        a = facade.get(amenity_id)
        if not a or not isinstance(a, Amenity):
            return {"error": "Amenity not found"}, 404

        facade.delete(amenity_id)
        return "", 204
