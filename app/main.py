from fastapi import FastAPI, Depends, HTTPException, status
from datetime import timedelta
from sqlalchemy.orm import Session
from . import rest, models, schemas, database; from .schemas import LoginRequest
from .models import User; from .rest import get_user
from .auth import get_current_active_admin
from .database import engine, get_db
from typing import List
from .auth import create_access_token, verify_password, get_password_hash, get_current_user
import logging

from .routes import fuels

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Создание всех таблиц в БД
models.Base.metadata.create_all(bind=engine)

app = FastAPI()



# Создание нового пользователя
@app.post("/create-user/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username, 
        email=user.email, 
        password=hashed_password,
        role = user.role if user.role else "user")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

from sqlalchemy.orm import Session
from .models import User
from .auth import get_password_hash
from .database import get_db

# -----------------------------------------------------------------------------------------------------
# Функция для хэширования всех паролей, так как на этапе до внедрения токенов я пароли не хэшировал, то после внедрения токенов пришлось дописывать код, который бы хэшировал пароли, которые я не хэшировал (проще было бы бд снести и по новой создавать пользователей)
def hash_passwords(db: Session):
    users = db.query(User).all()  # Получаем всех пользователей
    for user in users:
        if not user.password.startswith("$2b$"):  # Проверяем, что пароль не хэширован (bcrypt хэши обычно начинаются с "$2b$")
            user.password = get_password_hash(user.password)  # Хэшируем пароль
    db.commit()  # Сохраняем изменения в базе данных
    print("Пароли успешно хэшированы.")

# Функция для запуска скрипта
def run_hashing():
    with next(get_db()) as db:  # Открываем сессию базы данных
        hash_passwords(db)  # Запускаем хэширование паролей
# run_hashing()
# -----------------------------------------------------------------------------------------------------

# Аутентификация пользователя
def authenticate_user(db: Session, username: str, password: str):
    user = rest.get_user_by_username(db, username)
    if not user or not verify_password(password, user.password):
        return False
    return user

# Проверка роли пользователя
def check_admin(user: schemas.User):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Admins only."
        )

# Эндпоинт для получения токена
@app.post("/token")
async def login_for_access_token(login_request: LoginRequest, db: Session = Depends(database.get_db)):
    user = authenticate_user(db, login_request.username, login_request.password)
    logger.info(f"ИНФААА: {login_request.username, login_request.password}")
    if not user:
        logger.debug(f"да бля")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=1200)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/admin/")
async def read_admin_data(current_user: User = Depends(get_current_active_admin)):
    return {"message": f"Hello, {current_user.username}. You have admin access."}

# Получение всех пользователей
@app.get("/admin/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_admin(current_user)
    users = rest.get_users(db, skip=skip, limit=limit)
    logger.warning(f"ИНФААА:")
    return users

# Получение пользователя по ID
@app.get("/admin/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = rest.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# штучка, которая позволяет подключить эндпоинты из другого файла
app.include_router(fuels.router)