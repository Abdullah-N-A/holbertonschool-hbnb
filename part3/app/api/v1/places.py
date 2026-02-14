# app/api/v1/places.py
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app.business.facade import HBnBFacade
from app.models.place import Place
from app.models.user import User
from app.models.review import Review
from app.extensions import db

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


    @jwt_required()
    def post(self, place_id):
        data = api.payload or {}

        text = (data.get("text") or "").strip()
        rating = data.get("rating")

        if not text:
            return {"error": "Text is required"}, 400
        
        # rating لازم رقم بين 1 و 5
        try:
            rating = int(rating)
        except Exception:
            return {"error": "Rating must be an integer"}, 400

        if rating < 1 or rating > 5:
            return {"error": "Rating must be between 1 and 5"}, 400

        place = Place.query.get(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404
            
        if getattr(user, "is_admin", False):
            return {"error": "Admins are not allowed to create reviews"}, 403

        review = Review(
            text=text,
            rating=rating,
            user_id=user_id,
            place_id=place_id
        )

        db.session.add(review)
        db.session.commit()

        return {
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "user_id": review.user_id,
            "place_id": review.place_id,
            "created_at": review.created_at.isoformat() if review.created_at else None,
            "updated_at": review.updated_at.isoformat() if review.updated_at else None,
        }, 201
