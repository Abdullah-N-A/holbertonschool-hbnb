"""
Models package initializer.

This module provides access to the core business logic models.
"""
from app.extensions import db
from .base_model import BaseModel
from .user import User
from .place import Place
from .review import Review
from .amenity import Amenity


__all__ = ["db", "BaseModel", "User", "Place", "Review", "Amenity"]
