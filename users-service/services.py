import os, jwt
from uuid import UUID
from datetime import datetime, timezone, timedelta

from typing import List, Optional, Annotated
from models import User
from schemas import CreateUserBase, UserLoginBase

from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from starlette import status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

ALGORITHM = "HS256"
SECRET_KEY = os.environ.get("SECRET_KEY")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Unable to validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
)

ACCESS_TOKEN_LIFETIME = timedelta(minutes=60)

def verify_password(plaintext_password, hashed_password) -> bool:
    return pwd_context.verify(plaintext_password, hashed_password)

def get_password_hash(password) -> str:
    return pwd_context.hash(password)

def fetch_all_users(token: Annotated[str, Depends(oauth2_scheme)], db: Session) -> List[dict]:
    try:
        users = db.query(User).filter(User.is_deleted == False).all()
        return [user.to_json() for user in users]
    except Exception:
        return credentials_exception

def fetch_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session) -> List[dict]:
    try:
        # get current user email
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        user = db.query(User).filter(User.is_deleted == False).filter(User.email == email).first()
        return user.to_json() if user else JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "User not found"}
        )
    except jwt.exceptions.InvalidTokenError:
        return credentials_exception

def fetch_user_by_id(token: Annotated[str, Depends(oauth2_scheme)], db: Session, id: UUID) -> Optional[dict]:
    user = db.query(User).filter(User.is_deleted == False).filter_by(id = id).first()
    return user.to_json() if user else JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": "User not found"}
    )

def login_user(db: Session, data: UserLoginBase) -> JSONResponse:
    user = db.query(User).filter(User.is_deleted == False).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        return JSONResponse (
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Invalid email or password"}
        )
    encode_data = user.to_json()
    expire_time = datetime.now(timezone.utc) + ACCESS_TOKEN_LIFETIME
    encode_data.update({"exp": expire_time})
    encoded_jwt = jwt.encode(encode_data, SECRET_KEY, algorithm=ALGORITHM)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"token": encoded_jwt, "id": str(user.id)}
    )

def create_new_user(db: Session, data: CreateUserBase):
    new_user = User(**data.model_dump())
    new_user.password = get_password_hash(new_user.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={ "message": "User created successfully" }
    )