from pydantic import BaseModel, EmailStr


# Schema for User creation
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


# Schema for User retrieval
class User(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


# Schema for Login
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Schema for JWT Response
class Token(BaseModel):
    access_token: str
    token_type: str
