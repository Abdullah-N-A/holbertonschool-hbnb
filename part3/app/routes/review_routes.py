from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Review, Place, User, db

review_bp = Blueprint('reviews', __name__)

# Create a review (owner restriction unless admin)
@review_bp.route('/', methods=['POST'])
@jwt_required()
def create_review():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    place = Place.query.get_or_404(data['place_id'])

    # Admin can bypass restrictions
    if not user.is_admin:
        if place.owner_id == user_id:
            return jsonify({"error": "You cannot review your own place"}), 403
        existing_review = Review.query.filter_by(user_id=user_id, place_id=place.id).first()
        if existing_review:
            return jsonify({"error": "You have already reviewed this place"}), 403

    new_review = Review(
        user_id=user_id,
        place_id=place.id,
        text=data['text'],
        rating=data.get('rating', 5)
    )

    db.session.add(new_review)
    db.session.commit()
    return jsonify(new_review.to_dict()), 201


# Update a review (owner OR admin)
@review_bp.route('/<int:review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    review = Review.query.get_or_404(review_id)

    # Admin can bypass ownership restriction
    if not user.is_admin and review.user_id != user_id:
        return jsonify({"error": "You can only edit your own reviews"}), 403

    data = request.get_json()
    review.text = data.get('text', review.text)
    review.rating = data.get('rating', review.rating)

    db.session.commit()
    return jsonify(review.to_dict()), 200
