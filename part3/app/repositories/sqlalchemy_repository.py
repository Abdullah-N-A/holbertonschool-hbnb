# app/repositories/sqlalchemy_repository.py
from app.models import db, User, Place, Review, Amenity

class SQLAlchemyRepository:
    """SQLAlchemy-based repository implementing CRUD operations"""

    # ---------- Users ----------
    def add_user(self, user):
        db.session.add(user)
        db.session.commit()
        return user

    def get_user_by_id(self, user_id):
        return User.query.get(user_id)

    def get_user_by_email(self, email):
        return User.query.filter_by(email=email).first()

    def update_user(self, user):
        db.session.commit()
        return user

    def delete_user(self, user):
        db.session.delete(user)
        db.session.commit()

    # ---------- Places ----------
    def add_place(self, place):
        db.session.add(place)
        db.session.commit()
        return place

    def get_place_by_id(self, place_id):
        return Place.query.get(place_id)

    def update_place(self, place):
        db.session.commit()
        return place

    def delete_place(self, place):
        db.session.delete(place)
        db.session.commit()

    # ---------- Reviews ----------
    def add_review(self, review):
        db.session.add(review)
        db.session.commit()
        return review

    def get_review_by_id(self, review_id):
        return Review.query.get(review_id)

    def update_review(self, review):
        db.session.commit()
        return review

    def delete_review(self, review):
        db.session.delete(review)
        db.session.commit()

    # ---------- Amenities ----------
    def add_amenity(self, amenity):
        db.session.add(amenity)
        db.session.commit()
        return amenity

    def get_amenity_by_id(self, amenity_id):
        return Amenity.query.get(amenity_id)

    def update_amenity(self, amenity):
        db.session.commit()
        return amenity

    def delete_amenity(self, amenity):
        db.session.delete(amenity)
        db.session.commit()
