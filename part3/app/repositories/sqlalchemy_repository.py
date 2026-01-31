# app/repositories/sqlalchemy_repository.py
from app.extensions import db
from app.models import User, Place, Review, Amenity


class SQLAlchemyRepository:
    """SQLAlchemy repository implementing CRUD for all entities"""

    # ---------- Users ----------
    def add_user(self, user: User) -> User:
        db.session.add(user)
        db.session.commit()
        return user

    def get_user_by_id(self, user_id: str):
        return User.query.get(user_id)

    def get_user_by_email(self, email: str):
        return User.query.filter_by(email=email).first()

    def list_users(self):
        return User.query.all()

    def update_user(self, user_id: str, data: dict):
        user = self.get_user_by_id(user_id)
        if not user:
            return None

        for key, value in (data or {}).items():
            if hasattr(user, key) and key not in ("id", "password"):
                setattr(user, key, value)

        db.session.commit()
        return user

    def delete_user(self, user_id: str) -> bool:
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        db.session.delete(user)
        db.session.commit()
        return True

    # ---------- Places ----------
    def add_place(self, place: Place) -> Place:
        db.session.add(place)
        db.session.commit()
        return place

    def get_place_by_id(self, place_id: str):
        return Place.query.get(place_id)

    def list_places(self):
        return Place.query.all()

    def update_place(self, place_id: str, data: dict):
        place = self.get_place_by_id(place_id)
        if not place:
            return None

        for key, value in (data or {}).items():
            if hasattr(place, key) and key != "id":
                setattr(place, key, value)

        db.session.commit()
        return place

    def delete_place(self, place_id: str) -> bool:
        place = self.get_place_by_id(place_id)
        if not place:
            return False
        db.session.delete(place)
        db.session.commit()
        return True

    # ---------- Reviews ----------
    def add_review(self, review: Review) -> Review:
        db.session.add(review)
        db.session.commit()
        return review

    def get_review_by_id(self, review_id: str):
        return Review.query.get(review_id)

    def list_reviews(self):
        return Review.query.all()

    def update_review(self, review_id: str, data: dict):
        review = self.get_review_by_id(review_id)
        if not review:
            return None

        for key, value in (data or {}).items():
            if hasattr(review, key) and key != "id":
                setattr(review, key, value)

        db.session.commit()
        return review

    def delete_review(self, review_id: str) -> bool:
        review = self.get_review_by_id(review_id)
        if not review:
            return False
        db.session.delete(review)
        db.session.commit()
        return True

    # ---------- Amenities ----------
    def add_amenity(self, amenity: Amenity) -> Amenity:
        db.session.add(amenity)
        db.session.commit()
        return amenity

    def get_amenity_by_id(self, amenity_id: str):
        return Amenity.query.get(amenity_id)

    def list_amenities(self):
        return Amenity.query.all()

    def update_amenity(self, amenity_id: str, data: dict):
        amenity = self.get_amenity_by_id(amenity_id)
        if not amenity:
            return None

        for key, value in (data or {}).items():
            if hasattr(amenity, key) and key != "id":
                setattr(amenity, key, value)

        db.session.commit()
        return amenity

    def delete_amenity(self, amenity_id: str) -> bool:
        amenity = self.get_amenity_by_id(amenity_id)
        if not amenity:
            return False
        db.session.delete(amenity)
        db.session.commit()
        return True
