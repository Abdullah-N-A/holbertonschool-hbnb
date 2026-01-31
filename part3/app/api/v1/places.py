# app/api/v1/places.py
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app.business.facade import HBnBFacade
from app.models.place import Place
from app.models.user import User

facade = HBnBFacade()
api = Namespace("places", description="Place operations")

place_model = api.model(
    "Place",
    {
        "name": fields.String(required=True),
        "description": fields.String(required=False),
        "city": fields.String(required=True),
        "price_per_night": fields.Float(required=True),
        "latitude": fields.Float(required=True),
        "longitude": fields.Float(required=True),
        # REMOVE owner_id from input for authenticated flow
    },
)

@api.route("/")
class PlaceList(Resource):
    def get(self):
        places = facade.get_places()
        return [{
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "city": p.city,
            "price_per_night": p.price_per_night,
            "latitude": p.latitude,
            "longitude": p.longitude,
            "owner_id": p.owner_id,
            "amenities": [a.id for a in (p.amenities or [])],
            "created_at": p.created_at.isoformat() if p.created_at else None,
            "updated_at": p.updated_at.isoformat() if p.updated_at else None,
        } for p in places], 200

    @jwt_required()
    @api.expect(place_model, validate=True)
    def post(self):
        data = api.payload or {}

        user_id = get_jwt_identity()
        owner = User.query.get(user_id)
        if not owner:
            return {"error": "Owner not found"}, 400

        new_place = Place(
            name=data["name"],
            description=data.get("description", ""),
            city=data["city"],
            price_per_night=data["price_per_night"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            owner_id=owner.id,
        )

        created = facade.create(new_place)
        return {
            "id": created.id,
            "name": created.name,
            "description": created.description,
            "city": created.city,
            "price_per_night": created.price_per_night,
            "latitude": created.latitude,
            "longitude": created.longitude,
            "owner_id": created.owner_id,
            "amenities": [a.id for a in (created.amenities or [])],
            "created_at": created.created_at.isoformat() if created.created_at else None,
            "updated_at": created.updated_at.isoformat() if created.updated_at else None,
        }, 201


@api.route("/<string:place_id>")
class PlaceResource(Resource):
    def get(self, place_id):
        p = Place.query.get(place_id)
        if not p:
            return {"error": "Place not found"}, 404
        return {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "city": p.city,
            "price_per_night": p.price_per_night,
            "latitude": p.latitude,
            "longitude": p.longitude,
            "owner_id": p.owner_id,
            "amenities": [a.id for a in (p.amenities or [])],
            "created_at": p.created_at.isoformat() if p.created_at else None,
            "updated_at": p.updated_at.isoformat() if p.updated_at else None,
        }, 200

    @jwt_required()
    @api.expect(place_model)
    def put(self, place_id):
        p = Place.query.get(place_id)
        if not p:
            return {"error": "Place not found"}, 404

        claims = get_jwt()
        user_id = get_jwt_identity()
        if not claims.get("is_admin") and p.owner_id != user_id:
            return {"error": "Forbidden"}, 403

        data = api.payload or {}
        # block owner_id edits
        data.pop("owner_id", None)
        updated = facade.update(place_id, data)

        return {
            "id": updated.id,
            "name": updated.name,
            "description": updated.description,
            "city": updated.city,
            "price_per_night": updated.price_per_night,
            "latitude": updated.latitude,
            "longitude": updated.longitude,
            "owner_id": updated.owner_id,
            "amenities": [a.id for a in (updated.amenities or [])],
            "created_at": updated.created_at.isoformat() if updated.created_at else None,
            "updated_at": updated.updated_at.isoformat() if updated.updated_at else None,
        }, 200


@api.route("/<string:place_id>/reviews")
class PlaceReviews(Resource):
    def get(self, place_id):
        place = Place.query.get(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        return [{
            "id": r.id,
            "text": r.text,
            "rating": r.rating,
            "user_id": r.user_id,
            "place_id": r.place_id,
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "updated_at": r.updated_at.isoformat() if r.updated_at else None,
        } for r in (place.reviews or [])], 200
