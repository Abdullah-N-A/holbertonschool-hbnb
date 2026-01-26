from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Place, User, db

place_bp = Blueprint('places', __name__)

# Create a new place (any authenticated user)
@place_bp.route('/', methods=['POST'])
@jwt_required()
def create_place():
    user_id = get_jwt_identity()
    data = request.get_json()

    new_place = Place(
        name=data['name'],
        description=data.get('description', ''),
        owner_id=user_id
    )

    db.session.add(new_place)
    db.session.commit()
    return jsonify(new_place.to_dict()), 201


# Update a place (owner OR admin)
@place_bp.route('/<int:place_id>', methods=['PUT'])
@jwt_required()
def update_place(place_id):
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    place = Place.query.get_or_404(place_id)

    # Admin can bypass ownership restriction
    if not user.is_admin and place.owner_id != user_id:
        return jsonify({"error": "You can only edit your own places"}), 403

    data = request.get_json()
    place.name = data.get('name', place.name)
    place.description = data.get('description', place.description)

    db.session.commit()
    return jsonify(place.to_dict()), 200
