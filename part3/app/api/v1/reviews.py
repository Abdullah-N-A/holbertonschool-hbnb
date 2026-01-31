# app/api/v1/reviews.py
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.business.facade import HBnBFacade
from app.models.review import Review
from app.models.user import User
from app.models.place import Place

facade = HBnBFacade()
api = Namespace("reviews", description="Review operations")

review_model = api.model(
    "Review",
    {
        "text": fields.String(required=True),
        "rating": fields.Integer(required=True),
        "place_id": fields.String(required=True),
    },
)

@api.route("/")
class ReviewList(Resource):
    def get(self):
        reviews = Review.query.all()
        return [{
            "id": r.id,
            "text": r.text,
            "rating": r.rating,
            "user_id": r.user_id,
            "place_id": r.place_id,
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "updated_at": r.updated_at.isoformat() if r.updated_at else None,
        } for r in reviews], 200

    @jwt_required()
    @api.expect(review_model, validate=True)
    def post(self):
        data = api.payload or {}

        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 400

        place = Place.query.get(data["place_id"])
        if not place:
            return {"error": "Place not found"}, 400

        new_review = Review(
            text=data["text"],
            rating=data["rating"],
            user_id=user.id,
            place_id=place.id,
        )

        created = facade.create(new_review)

        return {
            "id": created.id,
            "text": created.text,
            "rating": created.rating,
            "user_id": created.user_id,
            "place_id": created.place_id,
            "created_at": created.created_at.isoformat() if created.created_at else None,
            "updated_at": created.updated_at.isoformat() if created.updated_at else None,
        }, 201


@api.route("/<string:review_id>")
class ReviewResource(Resource):
    def get(self, review_id):
        r = Review.query.get(review_id)
        if not r:
            return {"error": "Review not found"}, 404
        return {
            "id": r.id,
            "text": r.text,
            "rating": r.rating,
            "user_id": r.user_id,
            "place_id": r.place_id,
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "updated_at": r.updated_at.isoformat() if r.updated_at else None,
        }, 200

    @jwt_required()
    def put(self, review_id):
        r = Review.query.get(review_id)
        if not r:
            return {"error": "Review not found"}, 404

        claims = get_jwt()
        user_id = get_jwt_identity()
        if not claims.get("is_admin") and r.user_id != user_id:
            return {"error": "Forbidden"}, 403

        data = api.payload or {}
        data.pop("user_id", None)
        data.pop("place_id", None)

        updated = facade.update(review_id, data)

        return {
            "id": updated.id,
            "text": updated.text,
            "rating": updated.rating,
            "user_id": updated.user_id,
            "place_id": updated.place_id,
            "created_at": updated.created_at.isoformat() if updated.created_at else None,
            "updated_at": updated.updated_at.isoformat() if updated.updated_at else None,
        }, 200

    @jwt_required()
    def delete(self, review_id):
        r = Review.query.get(review_id)
        if not r:
            return {"error": "Review not found"}, 404

        claims = get_jwt()
        user_id = get_jwt_identity()
        if not claims.get("is_admin") and r.user_id != user_id:
            return {"error": "Admin only"}, 403
        r = facade.get(review_id)
        if not r or not isinstance(r, Review):
            
            return {"error": "Review not found"}, 404

        facade.delete(review_id)
        return "", 204
