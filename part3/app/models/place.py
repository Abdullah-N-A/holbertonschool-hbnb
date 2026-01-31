# app/models/place.py
from app.extensions import db
from .base_model import BaseModel


place_amenities = db.Table(
    "place_amenities",
    db.Column("place_id", db.String(36), db.ForeignKey("places.id"), primary_key=True),
    db.Column("amenity_id", db.String(36), db.ForeignKey("amenities.id"), primary_key=True),
)

class Place(BaseModel):
    __tablename__ = "places"

    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(1024), default="", nullable=True)
    city = db.Column(db.String(128), nullable=False)
    price_per_night = db.Column(db.Float, nullable=False, default=0.0)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    # owner relationship
    owner_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)

    # relationships
    reviews = db.relationship("Review", backref="place", lazy=True, cascade="all, delete-orphan")
    amenities = db.relationship("Amenity", secondary=place_amenities, lazy="subquery",
                                backref=db.backref("places", lazy=True))

    def __init__(self, name, description, city, price_per_night, latitude, longitude, owner_id=None, **kwargs):
        super().__init__(**kwargs)

        if not name:
            raise ValueError("Place name is required")
        if price_per_night is not None and price_per_night < 0:
            raise ValueError("Price must be positive")
        if not (-90 <= latitude <= 90):
            raise ValueError("Invalid latitude")
        if not (-180 <= longitude <= 180):
            raise ValueError("Invalid longitude")

        self.name = name
        self.description = description
        self.city = city
        self.price_per_night = price_per_night
        self.latitude = latitude
        self.longitude = longitude

       
        if owner_id is not None:
            self.owner_id = owner_id

    def add_amenity(self, amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)
