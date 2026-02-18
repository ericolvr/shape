
""" sql alchmey models """
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class UserModel(Base):
    """ """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    email = Column(String(120), unique=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

