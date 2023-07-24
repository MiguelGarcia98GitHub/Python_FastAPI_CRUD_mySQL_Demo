from sqlalchemy.orm import Session
from sqlalchemy import and_
from . import models, schemas
from ...security.jwt import decode_token


def create_todo(db: Session, todo: schemas.TodoCreate, creator_id: int):
    db_todo = models.Todo(title=todo.title, creator_id=creator_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(db: Session, todo_id: int, todo_update: schemas.TodoCreate):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo is None:
        return None

    for var, value in vars(todo_update).items():
        setattr(todo, var, value) if value else None

    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def delete_todo(db: Session, todo_id: int):
    # Fetch the todo
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        return None
    else:
        db.delete(todo)
        db.commit()
        return todo


def get_todos_by_user_id(db: Session, creator_id: int):
    return db.query(models.Todo).filter(models.Todo.creator_id == creator_id).all()


def get_todo_by_id(db: Session, todo_id: int):
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()
