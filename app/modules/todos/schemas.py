from pydantic import BaseModel, EmailStr


# Schema for Todo Creation
class TodoCreate(BaseModel):
    title: str


# Schema for Todo Retrieval
class TodoResponse(TodoCreate):
    id: int
    creator_id: int

    class Config:
        from_attributes = True
