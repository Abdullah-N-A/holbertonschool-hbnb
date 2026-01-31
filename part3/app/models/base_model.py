# app/models/base_model.py
import uuid
from datetime import datetime
from app.extensions import db

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def to_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        # ISO format for datetime
        if "created_at" in data and data["created_at"]:
            data["created_at"] = data["created_at"].isoformat()
        if "updated_at" in data and data["updated_at"]:
            data["updated_at"] = data["updated_at"].isoformat()
        return data
