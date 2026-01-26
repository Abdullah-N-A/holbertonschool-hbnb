from flask import request, jsonify, abort
from app.models import User
from app import bcrypt
from flask_jwt_extended import create_access_token

@app.route('/api/v1/login', methods=['POST'])
def login():
    # Get JSON data from the request
    data = request.get_json()

    # Validate that both email and password are provided
    if not data or 'email' not in data or 'password' not in data:
        abort(400, description="Missing email or password")

    # Query the user by email
    user = User.query.filter_by(email=data['email']).first()

    # Check if user exists and password is correct
    if user is None or not user.check_password(data['password']):
        abort(401, description="Invalid credentials")

    # Create JWT access token with user's ID as identity
    access_token = create_access_token(identity=user.id)

    # Return the token in JSON response
    return jsonify(access_token=access_token), 200
