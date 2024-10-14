from sqlalchemy.orm import Session
from . import models, schemas
from datetime import date
from .models import User

# Создание пользователя
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        email=user.email,
        password=user.password,
        regdate=date.today(),
        role=user.role,
        loyaltylvl="1",  # Начальный уровень лояльности
        score=0          # Начальный счёт
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Получение пользователя по ID
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# Получение всех пользователей
def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

# Получение пользователя по имени
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

# ----------------------------------------------------------------------------------
# fuel
def get_fuels(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Fuel).offset(skip).limit(limit).all()
def get_fuel(db: Session, fuel_id: int):
    return db.query(models.Fuel).filter(models.Fuel.id == fuel_id).first()

# gases

def get_gases(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Gas).offset(skip).limit(limit).all()
def get_gas(db: Session, gas_id: int):
    return db.query(models.Gas).filter(models.Gas.id == gas_id).first()
# fdus

def get_fdus(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.FDU).offset(skip).limit(limit).all()
def get_fdu(db: Session, fdu_id: int):
    return db.query(models.FDU).filter(models.FDU.id == fdu_id).first()