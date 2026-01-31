# app/business/facade.py
from app.extensions import db
from app.models import User, Place, Review, Amenity


class HBnBFacade:
    """Facade connected directly to SQLAlchemy (DB persistence)"""

    def create(self, obj):
        db.session.add(obj)
        db.session.commit()
        return obj

    def get(self, obj_id):
        """Search for object in all models"""
        for model in (User, Place, Review, Amenity):
            obj = model.query.get(obj_id)
            if obj:
                return obj
        return None

    def get_all(self):
        """Return all objects (used by API filtering)"""
        return (
            User.query.all()
            + Place.query.all()
            + Review.query.all()
            + Amenity.query.all()
        )

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if not obj:
            return None

        for key, value in (data or {}).items():
            if hasattr(obj, key):
                setattr(obj, key, value)

        db.session.commit()
        return obj

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if not obj:
            return False

        db.session.delete(obj)
        db.session.commit()
        return True

    def get_places(self):
        """Used by places API"""
        return Place.query.all()
