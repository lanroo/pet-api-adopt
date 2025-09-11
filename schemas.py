from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime

from app_types import GenderEnum, SpeciesEnum, StatusEnum
from app_types.constants import (
    MAX_NAME_LENGTH, MAX_BREED_LENGTH, MAX_CITY_LENGTH, 
    MAX_DESCRIPTION_LENGTH, MAX_EMAIL_LENGTH, MAX_PHONE_LENGTH, 
    MAX_FULL_NAME_LENGTH, MIN_AGE_MONTHS, MAX_AGE_MONTHS
)

class PetBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=MAX_NAME_LENGTH)
    species: SpeciesEnum
    breed: Optional[str] = Field(None, max_length=MAX_BREED_LENGTH)
    age: Optional[float] = Field(None, ge=MIN_AGE_MONTHS, le=MAX_AGE_MONTHS)  # idade em meses
    gender: GenderEnum
    city: Optional[str] = Field(None, max_length=MAX_CITY_LENGTH)
    description: Optional[str] = Field(None, max_length=MAX_DESCRIPTION_LENGTH)
    photos: Optional[List[str]] = []

class PetCreate(PetBase):
    pass

class PetUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=MAX_NAME_LENGTH)
    species: Optional[SpeciesEnum] = None
    breed: Optional[str] = Field(None, max_length=MAX_BREED_LENGTH)
    age: Optional[float] = Field(None, ge=MIN_AGE_MONTHS, le=MAX_AGE_MONTHS)
    gender: Optional[GenderEnum] = None
    city: Optional[str] = Field(None, max_length=MAX_CITY_LENGTH)
    description: Optional[str] = Field(None, max_length=MAX_DESCRIPTION_LENGTH)
    photos: Optional[List[str]] = None
    status: Optional[StatusEnum] = None

class PetResponse(PetBase):
    id: int
    status: StatusEnum
    created_at: datetime
    updated_at: Optional[datetime] = None
    adopted_at: Optional[datetime] = None
    adopted_by: Optional[int] = None

    class Config:
        from_attributes = True

class PetFilter(BaseModel):
    species: Optional[SpeciesEnum] = None
    gender: Optional[GenderEnum] = None
    city: Optional[str] = None
    status: Optional[StatusEnum] = None
    min_age: Optional[float] = None  # em meses
    max_age: Optional[float] = None  # em meses

class UserBase(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=MAX_FULL_NAME_LENGTH)
    email: EmailStr = Field(..., max_length=MAX_EMAIL_LENGTH)
    phone: Optional[str] = Field(None, max_length=MAX_PHONE_LENGTH)
    city: Optional[str] = Field(None, max_length=MAX_CITY_LENGTH)

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=MAX_FULL_NAME_LENGTH)
    email: Optional[EmailStr] = Field(None, max_length=MAX_EMAIL_LENGTH)
    phone: Optional[str] = Field(None, max_length=MAX_PHONE_LENGTH)
    city: Optional[str] = Field(None, max_length=MAX_CITY_LENGTH)

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class AdoptRequest(BaseModel):
    user_id: int
