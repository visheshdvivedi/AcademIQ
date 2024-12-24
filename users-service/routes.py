from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, DataError

from jwt.exceptions import InvalidTokenError
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from schemas import CreateUserBase, UserLoginBase
from services import (
    fetch_user_by_id,
    fetch_all_users,
    fetch_current_user,
    create_new_user,
    login_user
)
from utils.database import get_db
from utils.exception_handling import (
    integrity_error_handler,
    data_error_handler,
    default_exception_handler
)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/user/test")
async def index():
    return {"message": "Users service is up and running"}

@router.get("/user")
async def get_all_users(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        return fetch_all_users(token, db)
    except Exception as e:
        return default_exception_handler(e)

@router.get("/user/me")
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        return fetch_current_user(token, db)
    except Exception as e:
        return default_exception_handler(e)

@router.get("/user/{id}")
async def get_user_by_id(id: UUID, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        return fetch_user_by_id(token, db, id)
    except Exception as e:
        return default_exception_handler(e)

@router.post("/user/login")
async def user_login(data: UserLoginBase, db: Session = Depends(get_db)):
    return login_user(db, data)

@router.post("/user")
async def create_user(data: CreateUserBase, db: Session = Depends(get_db)):
    try:
        return create_new_user(db, data)
    except IntegrityError as e:
        return integrity_error_handler(e)
    except DataError as e:
        return data_error_handler(e)