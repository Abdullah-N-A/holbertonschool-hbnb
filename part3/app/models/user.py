# app/models/user.py
from app.extensions import db, bcrypt
from .base_model import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # hashed password
    first_name = db.Column(db.String(128), default="", nullable=False)
    last_name = db.Column(db.String(128), default="", nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    # Relationships (بتفيدك في التاسكات الجاية)
    places = db.relationship("Place", backref="owner", lazy=True)
    reviews = db.relationship("Review", backref="user", lazy=True)

    def hash_password(self, plain_password: str):
        self.password = bcrypt.generate_password_hash(plain_password).decode("utf-8")

    def verify_password(self, plain_password: str) -> bool:
        return bcrypt.check_password_hash(self.password, plain_password)
