# app/models/review.py
from app.extensions import db
from .base_model import BaseModel

class Review(BaseModel):
    __tablename__ = "reviews"

    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey("places.id"), nullable=False)

    def __init__(self, text, rating, user_id=None, place_id=None, **kwargs):
        super().__init__(**kwargs)

        if not text:
            raise ValueError("Review text is required")
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

        self.text = text
        self.rating = rating

       
        if user_id is not None:
            self.user_id = user_id
        if place_id is not None:
            self.place_id = place_id
