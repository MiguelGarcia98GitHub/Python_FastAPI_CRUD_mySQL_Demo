from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ...db.dbconnect import Base


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    title = Column(String(50))

    creator_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates="my_todos")
