# app/api/v1/places.py
from flask_restx import Namespace, Resource, fields
from app.business.facade import HBnBFacade
from app.models.place import Place
from app.models.user import User

facade = HBnBFacade()

api = Namespace("places", description="Place operations")

place_model = api.model(
    "Place",
    {
        "name": fields.String(required=True, description="Name of the place"),
        "description": fields.String(required=False, description="Description of the place"),
        "city": fields.String(required=True, description="City where the place is located"),
        "price_per_night": fields.Float(required=True, description="Price per night"),
        "latitude": fields.Float(required=True, description="Latitude of the place"),
        "longitude": fields.Float(required=True, description="Longitude of the place"),
        "owner_id": fields.String(required=True, description="ID of the owner (User)"),
    },
)


@api.route("/")
class PlaceList(Resource):
    @api.response(200, "List of places retrieved successfully")
    def get(self):
        """Retrieve all places"""
        places = facade.get_places()
        result = []
        for p in places:
            result.append(
                {
                    "id": p.id,
                    "name": p.name,
                    "description": p.description,
                    "city": p.city,
                    "price_per_night": p.price_per_night,
                    "latitude": p.latitude,
                    "longitude": p.longitude,
                    "owner_id": p.owner_id,  # ✅ SQLAlchemy column
                    "amenities": [a.id for a in (p.amenities or [])],
                    "created_at": p.created_at.isoformat() if p.created_at else None,
                    "updated_at": p.updated_at.isoformat() if p.updated_at else None,
                }
            )
        return result, 200

    @api.expect(place_model, validate=True)
    @api.response(201, "Place successfully created")
    @api.response(400, "Invalid input data")
    def post(self):
        """Create a new place"""
        data = api.payload or {}

        required_fields = ["name", "city", "price_per_night", "latitude", "longitude", "owner_id"]
        for field in required_fields:
            if field not in data:
                return {"error": f"{field} is required"}, 400

        # ✅ Validate owner exists using SQLAlchemy directly
        owner = User.query.get(data["owner_id"])
        if not owner:
            return {"error": "Owner not found"}, 400

        new_place = Place(
            name=data["name"],
            description=data.get("description", ""),
            city=data["city"],
            price_per_night=data["price_per_night"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            owner_id=data["owner_id"],  # ✅ store FK
        )

        created_place = facade.create(new_place)

        return {
            "id": created_place.id,
            "name": created_place.name,
            "description": created_place.description,
            "city": created_place.city,
            "price_per_night": created_place.price_per_night,
            "latitude": created_place.latitude,
            "longitude": created_place.longitude,
            "owner_id": created_place.owner_id,  # ✅
            "amenities": [a.id for a in (created_place.amenities or [])],
            "created_at": created_place.created_at.isoformat() if created_place.created_at else None,
            "updated_at": created_place.updated_at.isoformat() if created_place.updated_at else None,
        }, 201


@api.route("/<string:place_id>")
class PlaceResource(Resource):
    @api.response(200, "Place details retrieved successfully")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Get place by ID"""
        p = facade.get(place_id)
        if not p or not isinstance(p, Place):
            return {"error": "Place not found"}, 404

        return {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "city": p.city,
            "price_per_night": p.price_per_night,
            "latitude": p.latitude,
            "longitude": p.longitude,
            "owner_id": p.owner_id,  # ✅
            "amenities": [a.id for a in (p.amenities or [])],
            "created_at": p.created_at.isoformat() if p.created_at else None,
            "updated_at": p.updated_at.isoformat() if p.updated_at else None,
        }, 200

    @api.expect(place_model)
    @api.response(200, "Place updated successfully")
    @api.response(404, "Place not found")
    @api.response(400, "Invalid input data")
    def put(self, place_id):
        """Update place"""
        p = facade.get(place_id)
        if not p or not isinstance(p, Place):
            return {"error": "Place not found"}, 404

        data = api.payload or {}
        updated_place = facade.update(place_id, data)

        return {
            "id": updated_place.id,
            "name": updated_place.name,
            "description": updated_place.description,
            "city": updated_place.city,
            "price_per_night": updated_place.price_per_night,
            "latitude": updated_place.latitude,
            "longitude": updated_place.longitude,
            "owner_id": updated_place.owner_id,  # ✅
            "amenities": [a.id for a in (updated_place.amenities or [])],
            "created_at": updated_place.created_at.isoformat() if updated_place.created_at else None,
            "updated_at": updated_place.updated_at.isoformat() if updated_place.updated_at else None,
        }, 200


@api.route("/<string:place_id>/reviews")
class PlaceReviews(Resource):
    @api.response(200, "List of reviews for the place")
    @api.response(404, "Place not found")
    def get(self, place_id):
        place = facade.get(place_id)
        if not place or not isinstance(place, Place):
            return {"error": "Place not found"}, 404

        # ✅ reviews relationship returns Review objects; use FK IDs
        return [
            {
                "id": r.id,
                "text": r.text,
                "rating": r.rating,
                "user_id": r.user_id,  # ✅
                "place_id": r.place_id,
                "created_at": r.created_at.isoformat() if r.created_at else None,
                "updated_at": r.updated_at.isoformat() if r.updated_at else None,
            }
            for r in (place.reviews or [])
        ], 200
