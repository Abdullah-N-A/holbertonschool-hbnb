from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.utils import admin_required
from app.models import Amenity, db

amenity_bp = Blueprint('amenities', __name__)

# Create a new amenity (Admin only)
@amenity_bp.route('/', methods=['POST'])
@jwt_required()
@admin_required
def create_amenity():
    data = request.get_json()
    new_amenity = Amenity(name=data['name'])
    db.session.add(new_amenity)
    db.session.commit()
    return jsonify(new_amenity.to_dict()), 201

# Update an existing amenity (Admin only)
@amenity_bp.route('/<int:amenity_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_amenity(amenity_id):
    amenity = Amenity.query.get_or_404(amenity_id)
    data = request.get_json()
    amenity.name = data.get('name', amenity.name)
    db.session.commit()
    return jsonify(amenity.to_dict()), 200
