from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, DataError

from fastapi import APIRouter, Depends

from schemas import CreateUserBase, UserLoginBase
from services import (
    fetch_user_by_id,
    fetch_all_users,
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

@router.get("/")
async def index():
    return {"message": "Users service is up and running"}

@router.get("/user")
async def get_all_users(db: Session = Depends(get_db)):
    return fetch_all_users(db)

@router.get("/user/{id}")
async def get_user_by_id(id: UUID, db: Session = Depends(get_db)):
    return fetch_user_by_id(db, id)

@router.post("/user/login")
async def user_login(data: UserLoginBase, db: Session = Depends(get_db)):
    try:
        return login_user(db, data)
    except Exception as e:
        print(e)
        return default_exception_handler(e)

@router.post("/user")
async def create_user(data: CreateUserBase, db: Session = Depends(get_db)):
    try:
        return create_new_user(db, data)
    except IntegrityError as e:
        return integrity_error_handler(e)
    except DataError as e:
        return data_error_handler(e)
    except Exception as e:
        print(e)
        return default_exception_handler(e)