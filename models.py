from sqlalchemy import Column, Integer, String, Float, Text, JSON, DateTime, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app_types import GenderEnum, SpeciesEnum, StatusEnum, AdoptionStatusEnum

Base = declarative_base()

class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    species = Column(Enum(SpeciesEnum), nullable=False)
    breed = Column(String(100))
    age = Column(Float)  # em meses
    gender = Column(Enum(GenderEnum), nullable=False)
    city = Column(String(100))
    description = Column(Text)
    photos = Column(JSON)  # Lista de URLs das fotos
    status = Column(Enum(StatusEnum), default=StatusEnum.AVAILABLE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    adopted_at = Column(DateTime, nullable=True)
    adopted_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    adopter = relationship("User", back_populates="adopted_pets")
    adoption_requests = relationship("AdoptionRequest", back_populates="pet")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(200), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)  # Senha hasheada
    whatsapp = Column(String(20))
    city = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    adopted_pets = relationship("Pet", back_populates="adopter")
    adoption_requests = relationship("AdoptionRequest", back_populates="user")


class AdoptionRequest(Base):
    __tablename__ = "adoption_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    full_name = Column(String(200), nullable=False)
    email = Column(String(255), nullable=False)
    whatsapp = Column(String(20))
    status = Column(Enum(AdoptionStatusEnum), default=AdoptionStatusEnum.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="adoption_requests")
    pet = relationship("Pet", back_populates="adoption_requests")
