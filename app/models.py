from sqlalchemy import Column,Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base

class Companie(Base):
    __tablename__ = "companie"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    name = Column(String)
    type = Column(String(100), nullable=False)
    region = Column(String(50), nullable=False)
    currency = Column(String(10), nullable=False)
    matchScore = Column(Float)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    type_id = Column(Integer, ForeignKey("user_type.id"))

class UserType(Base):
    __tablename__ = "user_type"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)

    user = relationship("User")
    

  



