from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Place, db

place_bp = Blueprint('places', __name__)

# إنشاء مكان
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

# تعديل مكان
@place_bp.route('/<int:place_id>', methods=['PUT'])
@jwt_required()
def update_place(place_id):
    user_id = get_jwt_identity()
    place = Place.query.get_or_404(place_id)
    if place.owner_id != user_id:
        return jsonify({"error": "يمكنك تعديل أماكنك فقط"}), 403
    data = request.get_json()
    place.name = data.get('name', place.name)
    place.description = data.get('description', place.description)
    db.session.commit()
    return jsonify(place.to_dict()), 200
