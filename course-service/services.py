import os, jwt
import requests
from uuid import UUID
from datetime import datetime, timezone, timedelta

from typing import List, Optional, Annotated
from models import Course
from schemas import CreateCourseSchema

from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from starlette import status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

ALGORITHM = "HS256"
SECRET_KEY = os.environ.get("SECRET_KEY")
USER_SERVICE_URL = os.environ.get("USER_SERVICE_URL")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Unable to validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
)

ACCESS_TOKEN_LIFETIME = timedelta(minutes=60)

def fetch_all_courses(db: Session):
    courses = db.query(Course).filter(Course.is_deleted == False).all()
    return [course.to_json() for course in courses]

def fetch_course_by_id(db: Session, course_id: UUID):
    return db.query(Course).filter(Course.is_deleted == False).filter(Course.id == str(course_id)).first()

def create_course(db: Session, data: CreateCourseSchema):
    new_course = Course(**data.model_dump())

    # validate instructor details
    import traceback
    try:
        response = requests.get(USER_SERVICE_URL + str(new_course.instructor_id))
        if not response.ok:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Invalid instructor ID"}
            )
        user_details = response.json()
        if "id" not in user_details or "first_name" not in user_details:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Failed to retrieve instructor details. Please try again"}
            )
        new_course.instructor_name = user_details.first_name + " " + user_details.last_name
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Failed to create course. Please try again"}
        )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course.to_json()