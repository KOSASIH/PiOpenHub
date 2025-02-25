# user_model .py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(length=50), nullable=False)
    email = Column(String(length=100), nullable=False)
    created_at = Column(DateTime, server_default=sa.func.now())

    def __repr__(self):
        return f"<User (id={self.id}, username='{self.username}', email='{self.email}')>"
