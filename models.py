from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Pet(Base):
    __tablename__ = "pets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    species = Column(String(50), nullable=False)  
    breed = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)  
    gender = Column(String(10), nullable=False) 
    status = Column(String(20), default="available")  
    city = Column(String(100), nullable=False)
    photos = Column(JSON, default=[])
    description = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    adopted_at = Column(DateTime, nullable=True)
    adopted_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    adopter = relationship("User", back_populates="adopted_pets")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(200), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    city = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    adopted_pets = relationship("Pet", back_populates="adopter")
