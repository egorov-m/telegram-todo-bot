from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Date
) 

from models import Base


class User(Base):
    __tablename__ = 'user'
    
    id: Column = Column('id', BigInteger, primary_key=True, nullable=False, autoincrement=True)
    telegram_user_id: Column = Column('telegram_user_id', BigInteger, unique=True, nullable=False)
    username: Column = Column('username', String, nullable=False)
    login: Column = Column('login', String, nullable=False)
    email: Column = Column('email', String, nullable=True)
    phone: Column = Column('phone', String, nullable=True)
    
    reg_date: Column = Column('reg_date', Date, nullable=False)
    upd_date: Column = Column('upd_date', Date, nullable=False)  # last update date
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, " \
               f"username={self.username!r}, " \
               f"login={self.login!r}, " \
               f"email={self.email!r}, " \
               f"phone={self.phone!r}, " \
               f"reg_date={self.reg_date!r}, " \
               f"upd_date={self.upd_date!r})" 
