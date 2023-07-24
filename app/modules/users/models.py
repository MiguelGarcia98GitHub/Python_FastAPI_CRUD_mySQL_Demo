from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ...db.dbconnect import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    hashed_password = Column(String(200))

    my_todos = relationship("Todo", back_populates="creator")
