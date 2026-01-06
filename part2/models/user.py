from models.base_model import BaseModel


class User(BaseModel):
    def __init__(self, email, password, first_name="", last_name=""):
        super().__init__()

        if not email:
            raise ValueError("Email is required")

        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.places = []
        self.reviews = []
