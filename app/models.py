from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from .database import Base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    regdate = Column(DateTime(timezone=True), default=func.now())
    role = Column(String, default="user")
    loyaltylvl = Column(String, default="1")
    score = Column(Integer, default=50)