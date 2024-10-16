from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from datetime import timedelta, datetime
from sqlalchemy.orm import Session
from .. import rest, models, schemas, database;
from ..models import User; from ..rest import get_user, get_gas
from ..auth import get_current_active_admin
from ..database import engine, get_db
from typing import List
from ..auth import create_access_token, verify_password, get_password_hash, get_current_user
import logging

router = APIRouter()

@router.post("/reviews/add/{id_gas}/",response_model=schemas.Review)
def create_review(id_gas: int, review: schemas.ReviewCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = current_user.id
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    db_review = models.Review(
        text = review.text,
        user_id = user,
        gas_id = id_gas,
        review_date = datetime.now(),
        gas = get_gas(db, id_gas)
    )
    
    # Создаем новый отзыв
    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    return db_review

# Получение всех reviews для конкретной gas 
@router.get("/gases/{gas_id}/reviews/", response_model=List[schemas.Review])
def read_reviews(gas_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    reviews = rest.get_reviews_by_gas_id(db, gas_id = gas_id, skip=skip, limit=limit)
    return reviews

# Получение review по ID
@router.get("/reviews/{reviews_id}", response_model=schemas.Review)
def read_review(reviews_id: int, db: Session = Depends(get_db)):
    db_review = rest.get_review(db, review_id=reviews_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review

@router.get("/reviews/", response_model=List[schemas.Review])
def read_reviews(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    reviews = rest.get_reviews(db, skip=skip, limit=limit)
    return reviews

@router.delete("/reviews/{reviews_id}", status_code=200)
def delete_review(reviews_id: int, db: Session = Depends(get_db)):
    # Найти заправку по её id
    review = db.query(models.Review).filter(models.Review.id == reviews_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    # Удалить заправку из базы данных
    db.delete(review)
    db.commit()

    return {"detail": f"Deleted Review with ID: {reviews_id}"}

@router.put("/reviews/{reviews_id}", status_code=200)
def update_review(reviews_id: int, review_data: schemas.ReviewUpdate, db: Session = Depends(get_db)):
    # Найти review по id
    review = db.query(models.Review).filter(models.Review.id == reviews_id).first()

    if not review:
        raise HTTPException(status_code=404, detail="review not found")

    # Обновить данные, если они были переданы
    if review_data.text is not None:
        review.text = review_data.text
        review.review_date = datetime.now()

    # Сохранить изменения в базе данных
    db.commit()
    db.refresh(review)

    return {"detail": "review updated successfully", "review": review}
