# app/models/amenity.py
from app.extensions import db
from .base_model import BaseModel

class Amenity(BaseModel):
    __tablename__ = "amenities"

    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(255), default="", nullable=True)

    def __repr__(self):
        return f"<Amenity {self.name}>"
