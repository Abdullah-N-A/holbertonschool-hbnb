from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

app = create_app()


def set_password(user, plain):
    if hasattr(user, "set_password"):
        user.set_password(plain)
    elif hasattr(user, "hash_password"):
        user.hash_password(plain)
    else:
        raise RuntimeError("User model has no set_password/hash_password method")


def reset_db():
    # FK order
    Review.query.delete()
    db.session.commit()

    Place.query.delete()
    db.session.commit()

    Amenity.query.delete()
    db.session.commit()

    User.query.delete()
    db.session.commit()


def get_or_create_user(email, first_name, last_name, password, is_admin=False, fixed_id=None):
    u = User.query.filter_by(email=email).first()
    if u:
        return u

    kwargs = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "is_admin": is_admin,
    }

    if fixed_id is not None:
        # if your model supports id as string/uuid
        kwargs["id"] = fixed_id

    u = User(**kwargs)
    set_password(u, password)
    db.session.add(u)
    db.session.commit()
    return u


def create_amenity(aid, name):
    # SQLAlchemy 2.x friendly: Session.get
    existing = db.session.get(Amenity, aid)
    if existing:
        return existing

    a = Amenity(id=aid, name=name)
    db.session.add(a)
    db.session.commit()
    return a


def safe_attach_amenities(place, amenities):
    # Only if relationship exists
    if hasattr(place, "amenities"):
        for a in amenities:
            place.amenities.append(a)
        db.session.commit()


def main():
    with app.app_context():
        # 0) wipe everything
        reset_db()

        # 1) users
        admin = get_or_create_user(
            email="admin@hbnb.io",
            first_name="Admin",
            last_name="HBnB",
            password="admin1234",
            is_admin=True,
            fixed_id="36c9050e-ddd3-4c3b-9731-9f487208bbc1"
        )

        owner = get_or_create_user(
            email="owner@hbnb.io",
            first_name="John",
            last_name="Doe",
            password="owner1234",
            is_admin=False
        )

        jane = get_or_create_user(
            email="jane@hbnb.io",
            first_name="Jane",
            last_name="Smith",
            password="jane1234",
            is_admin=False
        )

        robert = get_or_create_user(
            email="robert@hbnb.io",
            first_name="Robert",
            last_name="Brown",
            password="robert1234",
            is_admin=False
        )

        # 2) amenities
        wifi = create_amenity("a1b2c3d4-1111-2222-3333-444455556666", "WiFi")
        pool = create_amenity("b2c3d4e5-2222-3333-4444-555566667777", "Pool")
        ac   = create_amenity("c3d4e5f6-3333-4444-5555-666677778888", "Air Conditioning")
        kitchen = create_amenity("d4e5f6a7-4444-5555-6666-777788889999", "Kitchen")
        parking = create_amenity("e5f6a7b8-5555-6666-7777-888899990000", "Free Parking")
        gym = create_amenity("f6a7b8c9-6666-7777-8888-999900001111", "Gym")

        # 3) places (FULL - descriptions + city + coords)
        beach = Place(
            name="Beautiful Beach House",
            description=(
                "Wake up to ocean views and golden sunsets. This beach house is bright, airy, "
                "and designed for comfort—perfect for families or friends who want a relaxing stay "
                "steps away from the sea."
            ),
            city="Jeddah",
            price_per_night=150,
            latitude=21.4858,
            longitude=39.1925,
            owner_id=owner.id
        )

        cabin = Place(
            name="Cozy Cabin",
            description=(
                "A warm wooden cabin tucked away for a quiet escape. Enjoy fresh air, calm nights, "
                "and a comfortable interior with everything you need for a peaceful weekend."
            ),
            city="Abha",
            price_per_night=100,
            latitude=18.2164,
            longitude=42.5053,
            owner_id=owner.id
        )

        apt = Place(
            name="Modern Apartment",
            description=(
                "A clean, modern apartment in a convenient location. Bright living area, fast Wi-Fi, "
                "and a practical layout—ideal for business trips or a short city stay."
            ),
            city="Riyadh",
            price_per_night=200,
            latitude=24.7136,
            longitude=46.6753,
            owner_id=owner.id
        )

        db.session.add_all([beach, cabin, apt])
        db.session.commit()

        # 4) attach amenities (if relationship exists)
        safe_attach_amenities(beach, [wifi, pool, ac, kitchen, parking])
        safe_attach_amenities(cabin, [wifi, ac, parking])
        safe_attach_amenities(apt, [wifi, gym, parking, kitchen])

        # 5) reviews (NO ADMIN)
        # Beach
        db.session.add_all([
            Review(text="Great place to stay! Clean, beautiful, and the view is amazing.", rating=4, user_id=jane.id, place_id=beach.id),
            Review(text="Amazing location and very comfortable. Would definitely come back.", rating=5, user_id=robert.id, place_id=beach.id),
        ])

        # Cabin
        db.session.add_all([
            Review(text="Perfect for a weekend trip. Quiet and cozy with a great vibe.", rating=5, user_id=jane.id, place_id=cabin.id),
            Review(text="Nice place overall, super calm. Small improvements would make it perfect.", rating=4, user_id=robert.id, place_id=cabin.id),
        ])

        # Apartment
        db.session.add_all([
            Review(text="Clean and stylish. Wi-Fi was fast and the check-in was easy.", rating=5, user_id=jane.id, place_id=apt.id),
            Review(text="Great spot in the city. Comfortable and practical for a short stay.", rating=4, user_id=robert.id, place_id=apt.id),
        ])

        db.session.commit()

    print("✅ Database seeded successfully (full places + amenities + reviews).")


if __name__ == "__main__":
    main()
