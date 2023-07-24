from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from ...db.db_helpers import get_db
from ...security.jwt import decode_token
from . import schemas, services
from ..users.services import does_user_exist
from typing import List

router = APIRouter()


@router.post("/create", response_model=schemas.TodoResponse)
def create_todo(
    todo: schemas.TodoCreate,
    db: Session = Depends(get_db),
    authorization: str = Header(...),
):
    # Decode the token and get the user_id from it
    user_id = decode_token(authorization)

    # Check if the token is valid and contains a user_id
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid or missing token")

    # Check if the user actually exists in the database
    user_exists = does_user_exist(db, user_id)

    if user_exists is None:
        raise HTTPException(status_code=401, detail="That user does not exist")

    todo_creation = services.create_todo(db, todo, creator_id=user_id)
    return todo_creation


@router.put("/{todo_id}", response_model=schemas.TodoResponse)
def update_todo(
    todo_id: int,
    todo_update: schemas.TodoCreate,
    db: Session = Depends(get_db),
    authorization: str = Header(...),
):
    # Decode the token and get the user_id from it
    user_id = decode_token(authorization)

    # Check if the token is valid and contains a user_id
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid or missing token")

    # Check if the user actually exists in the database
    user_exists = does_user_exist(db, user_id)

    if user_exists is None:
        raise HTTPException(status_code=401, detail="That user does not exist")

    # Check if the todo actually exists and belongs to the user
    todo = services.get_todo_by_id(db, todo_id=todo_id)

    if todo is None or todo.creator_id != user_id:
        raise HTTPException(status_code=404, detail="Todo not found")

    updated_todo = services.update_todo(db, todo_id, todo_update)

    return updated_todo


@router.delete("/{todo_id}")
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    authorization: str = Header(...),
):
    # Decode the token and get the user_id from it
    user_id = decode_token(authorization)

    # Check if the token is valid and contains a user_id
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid or missing token")

    # Check if the user actually exists in the database
    user_exists = does_user_exist(db, user_id)

    if user_exists is None:
        raise HTTPException(status_code=401, detail="That user does not exist")

    todo = services.get_todo_by_id(db, todo_id)

    if not todo or todo.creator_id != user_id:
        raise HTTPException(status_code=404, detail="Todo not found")

    services.delete_todo(db, todo_id)
    return {"detail": f"Todo with the title {todo.title} successfully deleted"}


@router.get("/get_by_user_id", response_model=List[schemas.TodoResponse])
def read_user_todos(
    db: Session = Depends(get_db),
    authorization: str = Header(...),
):
    # Decode the token and get the user_id from it
    user_id = decode_token(authorization)

    # Check if the token is valid and contains a user_id
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid or missing token")

    # Check if the user actually exists in the database
    user_exists = does_user_exist(db, user_id)

    if user_exists is None:
        raise HTTPException(status_code=401, detail="That user does not exist")

    todo_list = services.get_todos_by_user_id(db, creator_id=user_id)
    return todo_list
