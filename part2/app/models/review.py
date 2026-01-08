from .base_model import BaseModel
from .user import User
from .place import Place


class Review(BaseModel):
    def __init__(self, text, rating, user: User, place: Place):
        super().__init__()

        if not text:
            raise ValueError("Review text is required")

        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

        self.text = text
        self.rating = rating
        self.user = user
        self.place = place

        user.reviews.append(self)
        place.reviews.append(self)
