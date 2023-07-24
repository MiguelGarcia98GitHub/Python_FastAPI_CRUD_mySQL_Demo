from datetime import datetime, timedelta
import jwt
from typing import Optional
from fastapi import HTTPException
from jwt import PyJWTError


SECRET_KEY = "your-secret-key"  # Replace this with a strong secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 262800  # 6 months example


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[int]:
    try:
        # Check the token format
        if not token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid token format")

        # Remove `Bearer ` from the token
        token = token[7:]

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )
        return int(user_id)
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token or expired token")
