from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity


class Place(BaseModel):
    def __init__(self, name, description, city, price_per_night, owner: User):
        super().__init__()

        if not name:
            raise ValueError("Place name is required")
        if price_per_night < 0:
            raise ValueError("Price must be positive")

        self.name = name
        self.description = description
        self.city = city
        self.price_per_night = price_per_night
        self.owner = owner
        self.reviews = []
        self.amenities = []

        owner.places.append(self)

    def add_amenity(self, amenity: Amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)
