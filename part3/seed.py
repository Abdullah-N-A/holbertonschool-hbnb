from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

app = create_app()


def set_password(user, plain):
    # supports set_password() OR hash_password()
    if hasattr(user, "set_password"):
        user.set_password(plain)
    elif hasattr(user, "hash_password"):
        user.hash_password(plain)
    else:
        raise RuntimeError("User model has no set_password/hash_password method")


def reset_db():
    # wipe tables (order matters)
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

    # set fixed UUID if your User model allows it
    if fixed_id is not None:
        try:
            kwargs["id"] = fixed_id
        except Exception:
            pass

    u = User(**kwargs)
    set_password(u, password)
    db.session.add(u)
    db.session.commit()
    return u


def create_amenity(aid, name):
    # SQLAlchemy 2.x friendly:
    existing = db.session.get(Amenity, aid)
    if existing:
        return existing

    a = Amenity(id=aid, name=name)
    db.session.add(a)
    db.session.commit()
    return a


def main():
    with app.app_context():
        # 0) wipe
        reset_db()

        # 1) users (match screenshots)
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

        # 2) amenities (match screenshots)
        wifi = create_amenity("a1b2c3d4-1111-2222-3333-444455556666", "WiFi")
        pool = create_amenity("b2c3d4e5-2222-3333-4444-555566667777", "Pool")
        ac   = create_amenity("c3d4e5f6-3333-4444-5555-666677778888", "Air Conditioning")

        # 3) places (MATCH EXACT NAMES + PRICES + DESCRIPTIONS)
        # Place __init__ requires: name, description, city, price_per_night, latitude, longitude
        # and you have owner_id (from your earlier seed)
        beach = Place(
            name="Beautiful Beach House",
            description="A beautiful beach house with amazing views...",
            city="",
            price_per_night=150,
            latitude=0.0,
            longitude=0.0,
            owner_id=owner.id
        )

        cabin = Place(
            name="Cozy Cabin",
            description="",
            city="",
            price_per_night=100,
            latitude=0.0,
            longitude=0.0,
            owner_id=owner.id
        )

        apt = Place(
            name="Modern Apartment",
            description="",
            city="",
            price_per_night=200,
            latitude=0.0,
            longitude=0.0,
            owner_id=owner.id
        )

        db.session.add_all([beach, cabin, apt])
        db.session.commit()

        # attach amenities to beach if relationship exists
        # (if your Place model uses place.amenities relationship)
        if hasattr(beach, "amenities"):
            beach.amenities.extend([wifi, pool, ac])
            db.session.commit()

        # 4) reviews for beach (match screenshots)
        r1 = Review(
            text="Great place to stay!",
            rating=4,
            user_id=jane.id,
            place_id=beach.id
        )
        r2 = Review(
            text="Amazing location and very comfortable.",
            rating=5,
            user_id=robert.id,
            place_id=beach.id
        )
        db.session.add_all([r1, r2])
        db.session.commit()

    print("✅ Database seeded successfully (matches screenshots).")


if __name__ == "__main__":
    main()
