from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, db

user_bp = Blueprint('users', __name__)

@user_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_user():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    if 'username' in data:
        user.username = data['username']
    if 'bio' in data:
        user.bio = data['bio']

    db.session.commit()
    return jsonify(user.to_dict()), 200
