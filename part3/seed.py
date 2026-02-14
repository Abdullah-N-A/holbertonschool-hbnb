from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place

app = create_app()

with app.app_context():

    # ================= ADMIN =================
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

    # ================= OWNER =================
    owner = User.query.filter_by(email="owner@hbnb.io").first()
    if not owner:
        owner = User(
            first_name="Owner",
            last_name="User",
            email="owner@hbnb.io",
            is_admin=False
        )
        owner.set_password("owner1234")
        db.session.add(owner)

    db.session.commit()

    # ================= AMENITIES =================
    amenities = [
        ("a1b2c3d4-1111-2222-3333-444455556666", "WiFi"),
        ("b2c3d4e5-2222-3333-4444-555566667777", "Swimming Pool"),
        ("c3d4e5f6-3333-4444-5555-666677778888", "Air Conditioning"),
    ]

    for aid, name in amenities:
        if not Amenity.query.get(aid):
            db.session.add(Amenity(id=aid, name=name))

    db.session.commit()

    # ================= PLACES =================
    if Place.query.count() == 0:
        places = [
            Place(
                name="Cozy Studio",
                description="Small studio in Riyadh.",
                city="Riyadh",
                price_per_night=120,
                latitude=24.7136,
                longitude=46.6753,
                owner_id=owner.id
            ),
            Place(
                name="Beach House",
                description="Beautiful house in Jeddah.",
                city="Jeddah",
                price_per_night=350,
                latitude=21.4858,
                longitude=39.1925,
                owner_id=owner.id
            ),
            Place(
                name="Mountain Cabin",
                description="Relaxing cabin in Abha.",
                city="Abha",
                price_per_night=220,
                latitude=18.2164,
                longitude=42.5053,
                owner_id=owner.id
            ),
        ]
        db.session.add_all(places)

    db.session.commit()

print("Database seeded successfully")
