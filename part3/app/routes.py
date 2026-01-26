if 'password' not in data:
    abort(400, description="Missing password")

user = User(
    email=data['email'],
    first_name=data.get('first_name'),
    last_name=data.get('last_name')
)

user.set_password(data['password'])
user.save()

return jsonify(user.to_dict()), 201
