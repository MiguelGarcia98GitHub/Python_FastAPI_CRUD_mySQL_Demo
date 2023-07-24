from sqlalchemy.orm import Session
from sqlalchemy import and_
from . import models, schemas
from passlib.context import CryptContext
from datetime import timedelta
from ...security.jwt import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN_EXPIRE_MINUTES = 262800  # 6 months example


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        username=user.username, email=user.email, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, user_login: schemas.UserLogin):
    db_user = (
        db.query(models.User)
        .filter(and_(models.User.email == user_login.email))
        .first()
    )
    if not db_user:
        return None
    if not pwd_context.verify(user_login.password, db_user.hashed_password):
        return None

    # Generate access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        {"sub": db_user.id, "email": db_user.email, "username": db_user.username},
        expires_delta=access_token_expires,
    )

    return access_token


# Internal functions:


def does_user_exist(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()
