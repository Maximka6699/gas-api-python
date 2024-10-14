from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from datetime import timedelta
from sqlalchemy.orm import Session
from .. import rest, models, schemas, database;
from ..models import User; from ..rest import get_user
from ..auth import get_current_active_admin
from ..database import engine, get_db
from typing import List
from ..auth import create_access_token, verify_password, get_password_hash, get_current_user
import logging

router = APIRouter()

@router.post("/fuels/add/",response_model=schemas.Fuel)
def add_fuel(fuel: schemas.FuelCreate, db: Session = Depends(database.get_db)):
    db_fuel = models.Fuel(name = fuel.name, price = fuel.price)
    # Получение FDU по переданным ID и добавление их к топливу
    if fuel.fdus:
        for fdu_id in fuel.fdus:
            fdu = db.query(models.FDU).filter(models.FDU.id == fdu_id).first()
            if not fdu:
                raise HTTPException(status_code=404, detail=f"FDU with id {fdu_id} not found")
            db_fuel.fdus.append(fdu)

    db.add(db_fuel)
    db.commit()
    db.refresh(db_fuel)
    return db_fuel

# Получение всех видов топлива
@router.get("/fuels/", response_model=List[schemas.Fuel])
def read_fuels(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    fuels = rest.get_fuels(db, skip=skip, limit=limit)
    return fuels

# Получение топлива по ID
@router.get("/fuels/{fuel_id}", response_model=schemas.Fuel)
def read_fuel(fuel_id: int, db: Session = Depends(get_db)):
    db_fuel1 = rest.get_fuel(db, fuel_id=fuel_id)
    if db_fuel1 is None:
        raise HTTPException(status_code=404, detail="Fuel not found")
    return db_fuel1

@router.delete("/fuels/{fuel_id}", status_code=200)
def delete_fuel(fuel_id: int, db: Session = Depends(get_db)):
    # Найти топливо по его id
    fuel = db.query(models.Fuel).filter(models.Fuel.id == fuel_id).first()
    
    if not fuel:
        raise HTTPException(status_code=404, detail="Fuel not found")

    # Удалить топливо из базы данных
    db.delete(fuel)
    db.commit()

    return print("Fuel deleted successfully")

@router.put("/fuels/{fuel_id}", status_code=200)
def update_fuel(fuel_id: int, fuel_data: schemas.FuelUpdate, db: Session = Depends(get_db)):
    # Найти топливо по id
    fuel = db.query(models.Fuel).filter(models.Fuel.id == fuel_id).first()

    if not fuel:
        raise HTTPException(status_code=404, detail="Fuel not found")

    # Обновить данные, если они были переданы
    if fuel_data.name is not None:
        fuel.name = fuel_data.name
    if fuel_data.price is not None:
        fuel.price = fuel_data.price
    if fuel_data.fdus is not [None]:
        for fdu_id in fuel_data.fdus:
            fdu = db.query(models.FDU).filter(models.FDU.id == fdu_id).first()
            if not fdu:
                raise HTTPException(status_code=404, detail=f"FDU with id {fdu_id} not found, {fuel_data.fdus, fdu} ")
            fuel.fdus.append(fdu)

    # Сохранить изменения в базе данных
    db.commit()
    db.refresh(fuel)

    return {"detail": "Fuel updated successfully", "fuel": fuel}