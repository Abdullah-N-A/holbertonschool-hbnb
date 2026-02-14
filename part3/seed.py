from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

app = create_app()


# ---------- helpers ----------
def set_password(user, plain):
    # supports set_password() OR hash_password()
    if hasattr(user, "set_password"):
        user.set_password(plain)
    elif hasattr(user, "hash_password"):
        user.hash_password(plain)
    else:
        raise RuntimeError("User model has no set_password/hash_password method")


def set_attr_if_exists(obj, attr, value):
    if hasattr(obj, attr):
        setattr(obj, attr, value)
        return True
    return False


def get_or_create_user(email, first_name, last_name, password, is_admin=False, fixed_id=None):
    u = User.query.filter_by(email=email).first()
    if u:
        return u

    kwargs = {}
    if fixed_id and hasattr(User, "id"):
        kwargs["id"] = fixed_id

    u = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        is_admin=is_admin,
        **kwargs
    )
    set_password(u, password)
    db.session.add(u)
    db.session.commit()
    return u


def get_or_create_amenity(aid, name):
    a = Amenity.query.get(aid) if hasattr(Amenity, "query") else None
    if a:
        return a

    # if your Amenity model doesn't use string id, it will ignore 'id' safely
    kwargs = {}
    if hasattr(Amenity, "id"):
        kwargs["id"] = aid

    a = Amenity(name=name, **kwargs)
    db.session.add(a)
    db.session.commit()
    return a


def wipe_db():
    # order matters بسبب FK
    try:
        Review.query.delete()
        db.session.commit()
    except Exception:
        db.session.rollback()

    try:
        # if you have association table, it will be handled by cascade, otherwise ignore
        Place.query.delete()
        db.session.commit()
    except Exception:
        db.session.rollback()

    try:
        Amenity.query.delete()
        db.session.commit()
    except Exception:
        db.session.rollback()

    try:
        User.query.delete()
        db.session.commit()
    except Exception:
        db.session.rollback()


def create_place(data, owner, amenities_objs):
    p = Place()

    # name/title
    if not set_attr_if_exists(p, "name", data["name"]):
        set_attr_if_exists(p, "title", data["name"])

    # description
    set_attr_if_exists(p, "description", data.get("description", ""))

    # price
    set_attr_if_exists(p, "price_per_night", data["price_per_night"])

    # location fields (optional)
    set_attr_if_exists(p, "city", data.get("city", ""))
    set_attr_if_exists(p, "country", data.get("country", ""))  # only if exists
    set_attr_if_exists(p, "latitude", data.get("latitude"))
    set_attr_if_exists(p, "longitude", data.get("longitude"))

    # owner/user id fields (different projects name it differently)
    if not set_attr_if_exists(p, "owner_id", owner.id):
        set_attr_if_exists(p, "user_id", owner.id)

    db.session.add(p)
    db.session.flush()  # get p.id

    # attach amenities if relationship exists
    if hasattr(p, "amenities") and data.get("amenities"):
        for a in amenities_objs:
            if a.name in data["amenities"]:
                p.amenities.append(a)

    db.session.commit()
    return p


def create_review(place, user, text, rating):
    r = Review()
    set_attr_if_exists(r, "text", text)
    set_attr_if_exists(r, "rating", rating)

    # link ids
    if hasattr(r, "place_id"):
        r.place_id = place.id
    if hasattr(r, "user_id"):
        r.user_id = user.id

    db.session.add(r)
    db.session.commit()
    return r


# ---------- seed data (matches screenshots) ----------
DATA = {
    "amenities": [
        ("a1b2c3d4-1111-2222-3333-444455556666", "WiFi"),
        ("b2c3d4e5-2222-3333-4444-555566667777", "Pool"),
        ("c3d4e5f6-3333-4444-5555-666677778888", "Air Conditioning"),
    ],
    "users": {
        "admin": {
            "id": "36c9050e-ddd3-4c3b-9731-9f487208bbc1",
            "first_name": "Admin",
            "last_name": "HBnB",
            "email": "admin@hbnb.io",
            "password": "admin1234",
            "is_admin": True
        },
        "owner": {
            "first_name": "John",
            "last_name": "Doe",
            "email": "owner@hbnb.io",
            "password": "owner1234",
            "is_admin": False
        },
        "jane": {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@hbnb.io",
            "password": "jane1234",
            "is_admin": False
        },
        "robert": {
            "first_name": "Robert",
            "last_name": "Brown",
            "email": "robert@hbnb.io",
            "password": "robert1234",
            "is_admin": False
        },
    },
    "places": [
        {
            "name": "Beautiful Beach House",
            "price_per_night": 150,
            "description": "A beautiful beach house with amazing views...",
            "amenities": ["WiFi", "Pool", "Air Conditioning"],
            # optional fields (only if your model has them)
            "city": "",
            "country": "",
            "latitude": None,
            "longitude": None,
        },
        {
            "name": "Cozy Cabin",
            "price_per_night": 100,
            "description": "",
            "amenities": [],
            "city": "",
            "country": "",
            "latitude": None,
            "longitude": None,
        },
        {
            "name": "Modern Apartment",
            "price_per_night": 200,
            "description": "",
            "amenities": [],
            "city": "",
            "country": "",
            "latitude": None,
            "longitude": None,
        },
    ],
    "reviews": [
        {
            "place_name": "Beautiful Beach House",
            "user_key": "jane",
            "text": "Great place to stay!",
            "rating": 4
        },
        {
            "place_name": "Beautiful Beach House",
            "user_key": "robert",
            "text": "Amazing location and very comfortable.",
            "rating": 5
        }
    ]
}


def main():
    with app.app_context():
        # wipe everything
        wipe_db()

        # users
        admin = get_or_create_user(
            email=DATA["users"]["admin"]["email"],
            first_name=DATA["users"]["admin"]["first_name"],
            last_name=DATA["users"]["admin"]["last_name"],
            password=DATA["users"]["admin"]["password"],
            is_admin=True,
            fixed_id=DATA["users"]["admin"]["id"],
        )
        owner = get_or_create_user(
            email=DATA["users"]["owner"]["email"],
            first_name=DATA["users"]["owner"]["first_name"],
            last_name=DATA["users"]["owner"]["last_name"],
            password=DATA["users"]["owner"]["password"],
            is_admin=False,
        )
        jane = get_or_create_user(
            email=DATA["users"]["jane"]["email"],
            first_name=DATA["users"]["jane"]["first_name"],
            last_name=DATA["users"]["jane"]["last_name"],
            password=DATA["users"]["jane"]["password"],
            is_admin=False,
        )
        robert = get_or_create_user(
            email=DATA["users"]["robert"]["email"],
            first_name=DATA["users"]["robert"]["first_name"],
            last_name=DATA["users"]["robert"]["last_name"],
            password=DATA["users"]["robert"]["password"],
            is_admin=False,
        )

        # amenities
        amenity_objs = []
        for aid, name in DATA["amenities"]:
            amenity_objs.append(get_or_create_amenity(aid, name))

        # places
        place_by_name = {}
        for p in DATA["places"]:
            place = create_place(p, owner=owner, amenities_objs=amenity_objs)
            place_by_name[p["name"]] = place

        # reviews
        user_map = {"jane": jane, "robert": robert, "admin": admin, "owner": owner}
        for r in DATA["reviews"]:
            place = place_by_name.get(r["place_name"])
            user = user_map.get(r["user_key"])
            if place and user:
                create_review(place, user, r["text"], r["rating"])

    print("✅ Database wiped + seeded to match screenshots successfully.")


if __name__ == "__main__":
    main()
