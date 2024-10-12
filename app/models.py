from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, Float, Table
from .database import Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

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

class Review(Base):
    __tablename__ = "Reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.id'), index=True)
    gas_id = Column(Integer, ForeignKey('Gases.id'), index=True)
    text = Column(String)
    review_date = Column(DateTime(timezone=True), default=func.now())
    gas = relationship("Gas", back_populates="reviews")

class Gas(Base):
    __tablename__ = "Gases"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    adress = Column(String)
    photo = Column(String)
    reviews = relationship("Review", back_populates="gas")
    fdus = relationship("FDU", back_populates="gases")

class FDU(Base):
    __tablename__ = "FDUs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    gas_id = Column(Integer, ForeignKey('Gases.id'), index=True)
    service_date = Column(DateTime(timezone=True), default=func.now())
    gases = relationship("Gas", back_populates="fdus")
    fuels = relationship("Fuel", secondary="fuel_fdu", back_populates="fdus")

class Fuel(Base):
    __tablename__ = "Fuels"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    price = Column(Float)
    fdus_id = Column(Integer, ForeignKey('FDUs.id'))
    fdus = relationship("FDU", secondary="fuel_fdu", back_populates="fuels")

# ----------------------------------------------------------------

fuel_fdu = Table(
    'fuel_fdu', Base.metadata,
    Column('fuel_id', Integer, ForeignKey('Fuels.id'), primary_key=True),
    Column('fdu_id', Integer, ForeignKey('FDUs.id'), primary_key=True)
)