""" Base model file """

from sqlalchemy.orm import declared_attr
from sqlmodel import SQLModel


class Base(SQLModel):
    """Abstract model with declarative base functionality"""

    @classmethod
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __allow_unmapped__ = False
