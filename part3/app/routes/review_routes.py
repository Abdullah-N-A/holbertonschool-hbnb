from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Place, Review, db

review_bp = Blueprint('reviews', __name__)

@review_bp.route('/', methods=['POST'])
@jwt_required()
def create_review():
    user_id = get_jwt_identity()
    data = request.get_json()
    place = Place.query.get_or_404(data['place_id'])

    if place.owner_id == user_id:
        return jsonify({"error": "لا يمكنك تقييم مكانك"}), 403

    existing_review = Review.query.filter_by(user_id=user_id, place_id=place.id).first()
    if existing_review:
        return jsonify({"error": "لقد قمت بتقييم هذا المكان مسبقاً"}), 403

    new_review = Review(
        user_id=user_id,
        place_id=place.id,
        text=data['text'],
        rating=data.get('rating', 5)
    )
    db.session.add(new_review)
    db.session.commit()
    return jsonify(new_review.to_dict()), 201
