from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class PetBase(BaseModel):
    name: str
    species: str  
    breed: str
    age: int
    gender: str 
    city: str
    description: Optional[str] = None

class PetCreate(PetBase):
    status: Optional[str] = "available"

class PetUpdate(BaseModel):
    name: Optional[str] = None
    species: Optional[str] = None
    breed: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    status: Optional[str] = None
    city: Optional[str] = None
    description: Optional[str] = None

class PetResponse(PetBase):
    id: int
    status: str
    photos: List[str] = []
    created_at: datetime
    updated_at: datetime
    adopted_at: Optional[datetime] = None
    adopted_by: Optional[int] = None
    
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    city: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    city: Optional[str] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class AdoptRequest(BaseModel):
    user_id: int
