from sqlalchemy import Identity

from fullask_rest_framework.factory.extensions import db


class BaseModel(db.Model):  # type: ignore[name-defined]
    """Parent model of all models"""

    __abstract__ = True

    id = db.Column(db.Integer, Identity(start=42, cycle=True), primary_key=True)
