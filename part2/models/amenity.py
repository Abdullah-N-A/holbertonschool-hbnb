from models.base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()

        if not name:
            raise ValueError("Amenity name is required")

        self.name = name
        self.description = description
