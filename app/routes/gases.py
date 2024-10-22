from fastapi import FastAPI, Depends, HTTPException, status, APIRouter, UploadFile, File
from datetime import timedelta
from sqlalchemy.orm import Session
from .. import rest, models, schemas, database;
from ..models import User; from ..rest import get_user
from ..auth import get_current_active_admin
from ..database import engine, get_db
from typing import List
from ..auth import create_access_token, verify_password, get_password_hash, get_current_user
import os, shutil, logging, json
# -*- coding: utf-8 -*-


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# Директория для сохранения изображений
UPLOAD_DIR = "pics"
os.makedirs(UPLOAD_DIR, exist_ok=True)


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

    image_paths = []
    # Обработка списка ссылок на локальные изображения
    for i in range(len(gas.photo)):
        photo_url = gas.photo[i]
        logger.debug(f"6: {gas.photo[i]}")
        if not os.path.exists(photo_url):
            raise HTTPException(status_code=400, detail=f"File {photo_url} does not exist")
        # Генерация уникального имени файла
        filename = os.path.basename(photo_url)
        destination_path = os.path.join(UPLOAD_DIR, filename)
        # Копирование файла в директорию сервера
        shutil.copy(photo_url, destination_path)
        logger.debug(f"{destination_path}")
        image_paths.append(destination_path)

    # Сохранение всех путей к изображениям в поле image_paths
    gas.photo = json.dumps(image_paths)
    
    # Создаем новую заправку
    db_gas = models.Gas(adress=gas.adress, photo=gas.photo, fdus=fdu_list, reviews=review_list)
    db.add(db_gas)
    db.commit()
    db.refresh(db_gas)

    return db_gas

@router.post("/gas/{gas_id}/upload-images/", status_code=200)
def upload_images(gas_id: int, photo: schemas.GasPhotos, db: Session = Depends(database.get_db)):
    gas = db.query(models.Gas).filter(models.Gas.id == gas_id).first()

    if not gas:
        raise HTTPException(status_code=404, detail="Gas station not found")

    image_paths = []
    # Обработка списка ссылок на локальные изображения
    for i in range(len(photo.photo)):
        photo_url = photo.photo[i]
        logger.debug(f"6: {photo.photo[i]}")


        if not os.path.exists(photo_url):
            raise HTTPException(status_code=400, detail=f"File {photo_url} does not exist")

        # Генерация уникального имени файла
        filename = os.path.basename(photo_url)
        destination_path = os.path.join(UPLOAD_DIR, filename)

        # Копирование файла в директорию сервера
        shutil.copy(photo_url, destination_path)
        logger.debug(f"{destination_path}")
        # gas.photo
        image_paths.append(destination_path)

    # Сохранение всех путей к изображениям в поле image_paths
    gas.photo = json.dumps(image_paths)
    logger.debug(f"1: {gas.photo}")

    db.commit()
    db.refresh(gas)
    return {"uploaded_files": image_paths, "photo_url": gas.photo}

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
        image_paths = []
        # Обработка списка ссылок на локальные изображения
        for i in range(len(gas_data.photo)):
            photo_url = gas_data.photo[i]
            if not os.path.exists(photo_url):
                raise HTTPException(status_code=400, detail=f"File {photo_url} does not exist")
            # Генерация уникального имени файла
            filename = os.path.basename(photo_url)
            destination_path = os.path.join(UPLOAD_DIR, filename)
            # Копирование файла в директорию сервера
            shutil.copy(photo_url, destination_path)
            logger.debug(f"{destination_path}")
            image_paths.append(destination_path)

        # Сохранение всех путей к изображениям в поле image_paths
        gas.photo = json.dumps(image_paths)
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
