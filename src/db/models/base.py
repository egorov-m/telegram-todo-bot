""" Base model file """

from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    """Abstract model with declarative base functionality"""

    @classmethod
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __allow_unmapped__ = False
