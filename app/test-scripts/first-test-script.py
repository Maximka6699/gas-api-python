from sqlalchemy.orm import Session
from datetime import datetime
import random
from ..database import SessionLocal
from ..models import User, Review, Gas, FDU, Fuel
from ..auth import get_password_hash

# Подключаемся к базе данных
db: Session = SessionLocal()

# Функция для добавления пользователей
def add_users(db: Session):
    users_data = [
        {"username": "admin1", "email": "admin1@example.com", "password": f"{get_password_hash('hashed_password')}", "role": "admin"},
        {"username": "admin2", "email": "admin2@example.com", "password": f"{get_password_hash('hashed_password')}", "role": "admin"},
        {"username": "user1", "email": "user1@example.com", "password": f"{get_password_hash('hashed_password')}", "role": "user"},
        {"username": "user2", "email": "user2@example.com", "password": f"{get_password_hash('hashed_password')}", "role": "user"},
        {"username": "user3", "email": "user3@example.com", "password": f"{get_password_hash('hashed_password')}", "role": "user"},
    ]
    for user_data in users_data:
        user = User(**user_data)
        db.add(user)
    db.commit()

# Функция для добавления заправок
def add_gases(db: Session):
    for i in range(5):
        gas = Gas(adress=f"Test Address {i + 1}", photo="[]")
        db.add(gas)
    db.commit()

# Функция для добавления FDU и привязки их к заправкам
def add_fdus(db: Session):
    gases = db.query(Gas).all()
    fdu_count = 20
    fdus = []
    
    for i in range(fdu_count):
        gas = random.choice(gases)
        fdu = FDU(gas_id=gas.id, service_date=datetime.now())
        db.add(fdu)
        fdus.append(fdu)
    db.commit()
    return fdus

# Функция для добавления видов топлива и привязки их к FDU
def add_fuels(db: Session):
    fdus = db.query(FDU).all()
    fuel_types = [
        {"name": "АИ-92", "price": 50.20},
        {"name": "ДТ", "price": 49.16},
        {"name": "АИ-95", "price": 65.90},
        {"name": "АИ-98", "price": 72.80},
    ]
    for fuel_data in fuel_types:
        fuel = Fuel(**fuel_data)
        db.add(fuel)
        db.commit()
    
    fuels = db.query(Fuel).all()
    
    for fdu in fdus:
        assigned_fuels = random.sample(fuels, k=random.randint(1, 3))
        fdu.fuels.extend(assigned_fuels)
    db.commit()

# Основная функция, добавляющая все данные
def populate_db():
    print("Добавляем пользователей...")
    add_users(db)
    print("Добавляем заправки...")
    add_gases(db)
    print("Добавляем FDU к заправкам...")
    fdus = add_fdus(db)
    print("Добавляем виды топлива и привязываем их к FDU...")
    add_fuels(db)
    print("Загрузка тестовых данных завершена!")

# Запуск функции заполнения
populate_db()
db.close()
