from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.db_helpers import get_db
from . import schemas, services


router = APIRouter()


@router.post("/register", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = services.get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=400, detail="User with this email already exists"
        )

    db_user = services.create_user(db, user)
    return db_user


@router.post("/login", response_model=schemas.Token)
def login(user_login: schemas.UserLogin, db: Session = Depends(get_db)):
    access_token = services.authenticate_user(db, user_login)

    if access_token is None:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return {"access_token": access_token, "token_type": "Bearer"}
