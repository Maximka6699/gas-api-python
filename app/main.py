from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import rest, models, schemas, database
from .database import engine, get_db
from typing import List
from .models import User 
from .schemas import UserCreate  

# Создание всех таблиц в БД
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Создание нового пользователя
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = models.User(
        username=user.username, 
        email=user.email, 
        password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Получение всех пользователей
@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = rest.get_users(db, skip=skip, limit=limit)
    return users

# Получение пользователя по ID
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = rest.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
