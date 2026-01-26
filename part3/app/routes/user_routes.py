from flask_jwt_extended import jwt_required
from app.utils import admin_required
from flask_bcrypt import generate_password_hash
from flask import request, jsonify
from app.models import User, db

@user_bp.route('/', methods=['POST'])
@jwt_required()
@admin_required  # This endpoint is restricted to admin users only
def create_user():
    """Create a new user – Admin only"""
    data = request.get_json()
    
    # Check if the email is already in use
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email is already in use"}), 400

    # Create a new user
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=generate_password_hash(data['password']).decode('utf-8'),
        is_admin=data.get('is_admin', False)
    )
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify(new_user.to_dict()), 201
