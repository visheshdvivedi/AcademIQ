import os, jwt
from uuid import UUID
from datetime import datetime, timezone, timedelta

from typing import List, Optional
from models import User
from schemas import CreateUserBase, UserLoginBase
from validations import validate_name, validate_email_address, validate_password

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from starlette import status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse


SECRET_KEY = os.environ.get("SECRET_KEY")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ACCESS_TOKEN_LIFETIME = timedelta(minutes=60)

def verify_password(plaintext_password, hashed_password) -> bool:
    return pwd_context.verify(plaintext_password, hashed_password)

def get_password_hash(password) -> str:
    return pwd_context.hash(password)

def fetch_all_users(db: Session) -> List[dict]:
    users = db.query(User).filter(User.is_deleted == False).all()
    return [user.to_json() for user in users]

def fetch_user_by_id(db: Session, id: UUID) -> Optional[dict]:
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
    encoded_jwt = jwt.encode(encode_data, SECRET_KEY, algorithm="HS256")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"token": encoded_jwt, "id": str(user.id)}
    )

def create_new_user(db: Session, data: CreateUserBase):
    new_user = User(**data.model_dump())

    # check for validation errors
    errors = []
    errors.extend(validate_name("first_name", new_user.first_name))
    errors.extend(validate_name("last_name", new_user.last_name))
    errors.extend(validate_email_address(new_user.email))
    errors.extend(validate_password(new_user.password))
    if len(errors):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": errors}
        )

    # set password hash
    new_user.password = get_password_hash(new_user.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={ "message": "User created successfully" }
    )