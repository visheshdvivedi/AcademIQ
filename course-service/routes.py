from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, DataError

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from schemas import CreateCourseSchema
from services import (
    fetch_all_courses,
    fetch_course_by_id,
    create_course
)
from utils.database import get_db
from utils.exception_handling import (
    integrity_error_handler,
    data_error_handler,
    default_exception_handler
)

router = APIRouter(prefix="/api/course")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/health")
async def index():
    return {"message": "Course service is up and running"}

@router.get("/")
async def get_all_courses(db: Session = Depends(get_db)):
    try:
        return fetch_all_courses(db)
    except Exception as e:
        return default_exception_handler(e)

@router.post("/create")
async def create_new_course(data: CreateCourseSchema, db: Session = Depends(get_db)):
    try:
        return create_course(db, data)
    except IntegrityError as e:
        return integrity_error_handler(e)
    except DataError as e:
        return data_error_handler(e)
    except Exception as e:
        return default_exception_handler(e)

@router.get("/{course_id}")
async def get_course_by_id(course_id: UUID, db: Session = Depends(get_db)):
    try:
        return fetch_course_by_id(db, course_id)
    except Exception as e:
        return default_exception_handler(e)