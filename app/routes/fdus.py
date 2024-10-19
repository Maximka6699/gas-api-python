from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from datetime import timedelta, datetime
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import rest, models, schemas, database;
from ..models import User; from ..rest import get_user
from ..auth import get_current_active_admin
from ..database import engine, get_db
from typing import List
from sqlalchemy.future import select
from ..auth import create_access_token, verify_password, get_password_hash, get_current_user


router = APIRouter()

def check_admin(user: schemas.User):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Admins only."
        )

@router.post("/fdus/add/",response_model=schemas.FDU)
def create_fdu(fdu: schemas.FDUCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_admin(current_user)
    # Проверяем, существует ли заправка
    if fdu.gas_id is not None:
        gas_station = db.query(models.Gas).filter(models.Gas.id == fdu.gas_id).first()
        if not gas_station:
            raise HTTPException(status_code=404, detail="Gas station not found")
    else:
        gas_station = None

    # Проверяем, существуют ли указанные виды топлива
    fuels_list = []
    for fuel_id in fdu.fuels:
        fuel = db.query(models.Fuel).filter(models.Fuel.id == fuel_id).first()
        if not fuel:
            raise HTTPException(status_code=404, detail=f"Fuel with id {fuel_id} not found")
        fuels_list.append(fuel)
    
    
    # Создаем новую FDU
    db_fdu = models.FDU(service_date=func.now(), gases=gas_station, fuels=fuels_list, gas_id=fdu.gas_id)
    db.add(db_fdu)
    db.commit()
    db.refresh(db_fdu)

    return db_fdu

# Получение всех ТРК
@router.get("/fdus/", response_model=List[schemas.FDU])
def read_fdus(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    fdus = rest.get_fdus(db, skip=skip, limit=limit)
    return fdus

# Получение ТРК по ID
@router.get("/fdus/{fdu_id}", response_model=schemas.FDU)
def read_fuel(fdu_id: int, db: Session = Depends(get_db)):
    db_fdu = rest.get_fdu(db, fdu_id=fdu_id)
    if db_fdu is None:
        raise HTTPException(status_code=404, detail="FDU not found")
    return db_fdu

@router.delete("/fdus/delete/", status_code=200)
def delete_fdus(fdu_ids: list[int], db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_admin(current_user)
    # Проверяем, есть ли FDU с данными ID
    stmt = select(models.FDU).where(models.FDU.id.in_(fdu_ids))
    result = db.execute(stmt)
    fdus_to_delete = result.scalars().all()

    if not fdus_to_delete:
        raise HTTPException(status_code=404, detail="FDU(s) not found")

    # Удаляем найденные FDU
    for fdu in fdus_to_delete:
        db.delete(fdu)

    db.commit()
    return {"detail": f"Deleted FDU(s) with IDs: {fdu_ids}"}

@router.put("/fdus/{fdu_id}", status_code=200)
def update_fdu(fdu_id: int, fdu_data: schemas.FDUUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_admin(current_user)
    # Найти FDU по id
    fdu = db.query(models.FDU).filter(models.FDU.id == fdu_id).first()
    if not fdu:
        raise HTTPException(status_code=404, detail="FDU not found")

    # Обновить данные, если они были переданы
    # обновляем id
    if fdu_data.id is not None:
        fdu.id = fdu_data.id
    # обновляем заправку к которой прикрепллена ТРК
    if fdu_data.gas_id is not None:
        gas_station = db.query(models.Gas).filter(models.Gas.id == fdu_data.gas_id).first()
        if not gas_station:
            raise HTTPException(status_code=404, detail="Gas station not found")
        fdu.gases = gas_station
    # Обновляем список доступного топлива
    if fdu_data.fuels is not None:
        fuels_list = []
        for fuel_id in fdu_data.fuels:
            fuel = db.query(models.Fuel).filter(models.Fuel.id == fuel_id).first()
            if not fuel:
                raise HTTPException(status_code=404, detail=f"Fuel with id {fuel_id} not found")
            fuels_list.append(fuel)
        fdu.fuels = fuels_list
    # обновляем дату обслуживания
    if fdu.service_date is not None:
        fdu.service_date = fdu_data.service_date
    else:
        fdu.service_date = datetime.now()    

    # Сохранить изменения в базе данных
    db.commit()
    db.refresh(fdu)

    return {"detail": "fdu updated successfully", "fdu": fdu}