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
