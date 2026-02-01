from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.amenity import Amenity

app = create_app()

with app.app_context():
    # Admin user
    admin = User.query.filter_by(email="admin@hbnb.io").first()
    if not admin:
        admin = User(
            id="36c9050e-ddd3-4c3b-9731-9f487208bbc1",
            first_name="Admin",
            last_name="HBnB",
            email="admin@hbnb.io",
            is_admin=True
        )
        admin.set_password("admin1234")
        db.session.add(admin)

    # Amenities
    amenities = [
        ("a1b2c3d4-1111-2222-3333-444455556666", "WiFi"),
        ("b2c3d4e5-2222-3333-4444-555566667777", "Swimming Pool"),
        ("c3d4e5f6-3333-4444-5555-666677778888", "Air Conditioning"),
    ]

    for aid, name in amenities:
        if not Amenity.query.get(aid):
            db.session.add(Amenity(id=aid, name=name))

    db.session.commit()

print("Database seeded successfully")
