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

@router.post("/gases/add/",response_model=schemas.Gas)
def create_gas(gas: schemas.GasCreate, db: Session = Depends(get_db)):
    # Проверяем, существуют ли указанные FDU
    fdu_list = []
    for fdu_id in gas.fdus:
        fdu = db.query(models.FDU).filter(models.FDU.id == fdu_id.id).first()
        if not fdu:
            raise HTTPException(status_code=404, detail=f"FDU with id {fdu_id.id} not found")
        fdu_list.append(fdu)

    # Проверяем, существуют ли указанные отзывы
    review_list = []
    for review_id in gas.reviews:
        review = db.query(models.FDU).filter(models.Review.id == review_id.id).first()
        if not review:
            raise HTTPException(status_code=404, detail=f"Review with id {review_id.id} not found")
        review_list.append(review)
    
    # Создаем новую заправку
    db_gas = models.Gas(adress=gas.adress, photo=gas.photo, fdus=fdu_list, reviews=review_list)
    db.add(db_gas)
    db.commit()
    db.refresh(db_gas)

    return db_gas

# Получение всех заправок
@router.get("/gases/", response_model=List[schemas.Gas])
def read_gases(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    gases = rest.get_gases(db, skip=skip, limit=limit)
    return gases

# Получение топлива по ID
@router.get("/gases/{gas_id}", response_model=schemas.Gas)
def read_fuel(gas_id: int, db: Session = Depends(get_db)):
    db_gas = rest.get_gas(db, gas_id=gas_id)
    if db_gas is None:
        raise HTTPException(status_code=404, detail="Gas not found")
    return db_gas

# @router.delete("/fuels/{fuel_id}", status_code=204)
# def delete_fuel(fuel_id: int, db: Session = Depends(get_db)):
#     # Найти топливо по его id
#     fuel = db.query(models.Fuel).filter(models.Fuel.id == fuel_id).first()
    
#     if not fuel:
#         raise HTTPException(status_code=404, detail="Fuel not found")

#     # Удалить топливо из базы данных
#     db.delete(fuel)
#     db.commit()

#     return print("Fuel deleted successfully")

# @router.put("/fuels/{fuel_id}", status_code=200)
# def update_fuel(fuel_id: int, fuel_data: schemas.FuelUpdate, db: Session = Depends(get_db)):
#     # Найти топливо по id
#     fuel = db.query(models.Fuel).filter(models.Fuel.id == fuel_id).first()

#     if not fuel:
#         raise HTTPException(status_code=404, detail="Fuel not found")

#     # Обновить данные, если они были переданы
#     if fuel_data.name is not None:
#         fuel.name = fuel_data.name
#     if fuel_data.price is not None:
#         fuel.price = fuel_data.price
#     if fuel.fdus is not None:
#         for fdu_id in fuel.fdus:
#             fdu = db.query(models.FDU).filter(models.FDU.id == fdu_id).first()
#             if not fdu:
#                 raise HTTPException(status_code=404, detail=f"FDU with id {fdu_id} not found")
#             fuel.fdus.append(fdu)

#     # Сохранить изменения в базе данных
#     db.commit()
#     db.refresh(fuel)

#     return {"detail": "Fuel updated successfully", "fuel": fuel}