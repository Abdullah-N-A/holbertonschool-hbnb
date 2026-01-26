# app/facade.py
from app.repositories.sqlalchemy_repository import SQLAlchemyRepository
from app.models import User

class HBNBFacade:
    """Facade class that uses SQLAlchemyRepository for persistence"""

    def __init__(self):
        self.repo = SQLAlchemyRepository()  # Use SQLAlchemy for all operations

    # ---------- Users ----------
    def create_user(self, username, email, password, is_admin=False):
        """Create a new user"""
        user = User(username=username, email=email, password=password, is_admin=is_admin)
        return self.repo.add_user(user)

    def get_user(self, user_id):
        """Retrieve a user by ID"""
        return self.repo.get_user_by_id(user_id)

    def update_user(self, user):
        """Update an existing user"""
        return self.repo.update_user(user)

    def delete_user(self, user):
        """Delete a user"""
        return self.repo.delete_user(user)

    # ---------- Places ----------
    def create_place(self, name, description, owner_id):
        from app.models import Place
        place = Place(name=name, description=description, owner_id=owner_id)
        return self.repo.add_place(place)

    def update_place(self, place):
        return self.repo.update_place(place)

    def delete_place(self, place):
        return self.repo.delete_place(place)

    # ---------- Reviews ----------
    def create_review(self, user_id, place_id, text, rating=5):
        from app.models import Review
        review = Review(user_id=user_id, place_id=place_id, text=text, rating=rating)
        return self.repo.add_review(review)

    def update_review(self, review):
        return self.repo.update_review(review)

    def delete_review(self, review):
        return self.repo.delete_review(review)

    # ---------- Amenities ----------
    def create_amenity(self, name):
        from app.models import Amenity
        amenity = Amenity(name=name)
        return self.repo.add_amenity(amenity)

    def update_amenity(self, amenity):
        return self.repo.update_amenity(amenity)

    def delete_amenity(self, amenity):
        return self.repo.delete_amenity(amenity)
