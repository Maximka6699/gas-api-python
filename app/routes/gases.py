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
def check_admin(user: schemas.User):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Admins only."
        )

@router.post("/gases/add/",response_model=schemas.Gas)
def create_gas(gas: schemas.GasCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_admin(current_user)
    # Проверяем, существуют ли указанные FDU
    fdu_list = []
    for fdu_id in gas.fdus:
        fdu = db.query(models.FDU).filter(models.FDU.id == fdu_id).first()
        if not fdu:
            raise HTTPException(status_code=404, detail=f"FDU with id {fdu_id} not found")
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
def read_gas(gas_id: int, db: Session = Depends(get_db)):
    db_gas = rest.get_gas(db, gas_id=gas_id)
    if db_gas is None:
        raise HTTPException(status_code=404, detail="Gas not found")
    return db_gas

@router.delete("/gases/{gas_id}", status_code=200)
def delete_gas(gas_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_admin(current_user)
    # Найти заправку по её id
    gas = db.query(models.Gas).filter(models.Gas.id == gas_id).first()
    if not gas:
        raise HTTPException(status_code=404, detail="Gas not found")

    # Удалить заправку из базы данных
    db.delete(gas)
    db.commit()

    return {"detail": f"Deleted Gas with ID: {gas_id} (вы удалили: {gas.adress})"}

@router.put("/gases/{gas_id}", status_code=200)
def update_gas(gas_id: int, gas_data: schemas.GasUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_admin(current_user)
    # Найти Gas по id
    gas = db.query(models.Gas).filter(models.Gas.id == gas_id).first()

    if not gas:
        raise HTTPException(status_code=404, detail="Gas not found")

    # Обновить данные, если они были переданы
    if gas_data.adress is not None:
        gas.adress = gas_data.adress
    if gas_data.photo is not None:
        gas.photo = gas_data.photo
    if gas_data.fdus is not [None]:
        for fdu_id in gas_data.fdus:
            fdu = db.query(models.FDU).filter(models.FDU.id == fdu_id).first()
            if not fdu:
                raise HTTPException(status_code=404, detail=f"FDU with id {fdu_id} not found")
            gas.fdus.append(fdu)
    if gas_data.reviews is not [None]:
        for review_id in gas_data.reviews:
            review = db.query(models.Review).filter(models.Review.id == review_id).first()
            if not review:
                raise HTTPException(status_code=404, detail=f"Review with id {review_id} not found")
            gas.reviews.append(review)

    # Сохранить изменения в базе данных
    db.commit()
    db.refresh(gas)

    return {"detail": "gas updated successfully", "gas": gas}
