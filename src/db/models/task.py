from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Boolean,
    ForeignKey
)

from dataclasses import dataclass
from src.db.models import Base


@dataclass
class Task(Base):
    __tablename__ = 'task'

    id: Column = Column('id', BigInteger, primary_key=True, unique=True, nullable=False, autoincrement=True)
    title: Column = Column('title', String, nullable=False)
    description: Column = Column('description', String, nullable=True)
    isDone: Column = Column('isDone', Boolean, nullable=False)

    id_user: Column = Column('id_user', BigInteger, ForeignKey(column="user.id"), nullable=False)

    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, title={self.title!r}, description={self.description!r}, isDone={self.isDone!r}, idUser={self.id_user!r})"
