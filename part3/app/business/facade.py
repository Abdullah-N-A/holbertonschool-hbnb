# app/business/facade.py
from app.repositories.sqlalchemy_repository import SQLAlchemyRepository
from app.models import User, Place, Review, Amenity


class HBnBFacade:
    """Facade layer using SQLAlchemyRepository"""

    def __init__(self):
        self.repo = SQLAlchemyRepository()

    # ---------- Create ----------
    def create(self, obj):
        cls_name = obj.__class__.__name__

        if cls_name == "User":
            return self.repo.add_user(obj)
        if cls_name == "Place":
            return self.repo.add_place(obj)
        if cls_name == "Review":
            return self.repo.add_review(obj)
        if cls_name == "Amenity":
            return self.repo.add_amenity(obj)

        raise ValueError(f"Unsupported object type: {cls_name}")

    # ---------- Read ----------
    def get(self, obj_id):
        for getter in (
            self.repo.get_user_by_id,
            self.repo.get_place_by_id,
            self.repo.get_review_by_id,
            self.repo.get_amenity_by_id,
        ):
            obj = getter(obj_id)
            if obj:
                return obj
        return None

    def get_all(self):
        return (
            self.repo.list_users()
            + self.repo.list_places()
            + self.repo.list_reviews()
            + self.repo.list_amenities()
        )

    def get_places(self):
        return self.repo.list_places()

    # ---------- Update ----------
    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if not obj:
            return None

        if isinstance(obj, User):
            return self.repo.update_user(obj_id, data)
        if isinstance(obj, Place):
            return self.repo.update_place(obj_id, data)
        if isinstance(obj, Review):
            return self.repo.update_review(obj_id, data)
        if isinstance(obj, Amenity):
            return self.repo.update_amenity(obj_id, data)

        return None

    # ---------- Delete ----------
    def delete(self, obj_id):
        obj = self.get(obj_id)
        if not obj:
            return False

        if isinstance(obj, User):
            return self.repo.delete_user(obj_id)
        if isinstance(obj, Place):
            return self.repo.delete_place(obj_id)
        if isinstance(obj, Review):
            return self.repo.delete_review(obj_id)
        if isinstance(obj, Amenity):
            return self.repo.delete_amenity(obj_id)

        return False
