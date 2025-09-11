from fastapi import FastAPI, Depends, HTTPException, Query, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import List, Optional
import os
import uuid
import shutil
from datetime import datetime

from database import get_db, init_db
from models import Pet, User, Base
from schemas import PetCreate, PetUpdate, UserCreate, UserUpdate, AdoptRequest

app = FastAPI(
    title="Pet Adoption API",
    description="""
    ## API para Sistema de Adoção de Pets
    
    Esta API permite:
    * Listar e buscar pets disponíveis
    * Cadastrar novos pets
    * Gerenciar usuários
    * Processar adoções
    * Visualizar estatísticas
    
    ### Como usar:
    1. Crie um usuário com `POST /users`
    2. Liste pets disponíveis com `GET /pets`
    3. Adote um pet com `POST /pets/{id}/adopt`
    """,
    version="1.0.0",
    contact={
        "name": "Pet Adoption Team",
        "email": "contato@petadoption.com",
    },
    license_info={
        "name": "MIT",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.on_event("startup")
async def startup_event():
    """Inicializar banco de dados na startup"""
    try:
        init_db()
        print("✅ Banco de dados inicializado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao inicializar banco: {e}")

@app.get("/health", tags=["Sistema"])
async def health_check():
    """
    Verificar se a API está funcionando
    """
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.get("/pets", tags=["Pets"])
async def list_pets(
    db: Session = Depends(get_db),
    species: Optional[str] = Query(None, description="Filtrar por espécie (dog, cat)"),
    city: Optional[str] = Query(None, description="Filtrar por cidade"),
    status: Optional[str] = Query(None, description="Filtrar por status (available, adopted)"),
    page: int = Query(1, ge=1, description="Número da página"),
    limit: int = Query(10, ge=1, le=100, description="Itens por página")
):
    """
    Listar todos os pets com filtros opcionais
    
    - **species**: dog, cat
    - **city**: qualquer cidade
    - **status**: available, adopted
    - **page**: paginação (começa em 1)
    - **limit**: máximo 100 itens por página
    """
    query = db.query(Pet)
    
    if species:
        query = query.filter(Pet.species == species)
    if city:
        query = query.filter(Pet.city.ilike(f"%{city}%"))
    if status:
        query = query.filter(Pet.status == status)
    
    total = query.count()
    offset = (page - 1) * limit
    pets = query.offset(offset).limit(limit).all()
    
    return {
        "pets": pets,
        "total": total,
        "page": page,
        "limit": limit
    }

@app.get("/pets/stats", tags=["Estatísticas"])
async def get_stats(db: Session = Depends(get_db)):
    """
    Obter estatísticas dos pets
    
    Retorna:
    - Total de pets
    - Pets disponíveis
    - Pets adotados
    """
    total = db.query(Pet).count()
    available = db.query(Pet).filter(Pet.status == "available").count()
    adopted = db.query(Pet).filter(Pet.status == "adopted").count()
    
    return {
        "total_pets": total,
        "available_pets": available,
        "adopted_pets": adopted
    }

@app.get("/pets/search", tags=["Pets"])
async def search_pets(q: str, db: Session = Depends(get_db)):
   
    pets = db.query(Pet).filter(
        or_(
            Pet.name.ilike(f"%{q}%"),
            Pet.breed.ilike(f"%{q}%"),
            Pet.city.ilike(f"%{q}%")
        )
    ).all()
    return {"pets": pets, "query": q}

@app.get("/pets/{pet_id}", tags=["Pets"])
async def get_pet(pet_id: int, db: Session = Depends(get_db)):
    
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    return pet

@app.post("/pets", status_code=201, tags=["Pets"])
async def create_pet(pet_data: PetCreate, db: Session = Depends(get_db)):
    """
    Cadastrar um novo pet
    
    Exemplo de dados:
    ```json
    {
        "name": "Luna",
        "species": "dog",
        "breed": "Golden Retriever",
        "age": 24,
        "gender": "female",
        "city": "São Paulo",
        "description": "Cadela muito carinhosa"
    }
    ```
    """
    pet_dict = pet_data.dict()
    pet = Pet(**pet_dict)
    pet.created_at = datetime.utcnow()
    pet.updated_at = datetime.utcnow()
    
    db.add(pet)
    db.commit()
    db.refresh(pet)
    return pet

@app.put("/pets/{pet_id}", tags=["Pets"])
async def update_pet(pet_id: int, pet_update: PetUpdate, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    
    update_data = pet_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(pet, key, value)
    
    pet.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(pet)
    return pet

@app.delete("/pets/{pet_id}", status_code=204, tags=["Pets"])
async def delete_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    
    db.delete(pet)
    db.commit()


@app.post("/pets/{pet_id}/adopt", tags=["Adoção"])
async def adopt_pet(pet_id: int, adopt_data: AdoptRequest, db: Session = Depends(get_db)):
    """
    Adotar um pet
    
    
    Exemplo de dados:
    ```json
    {
        "user_id": 1
    }
    ```
    """
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    
    if pet.status != "available":
        raise HTTPException(status_code=400, detail="Pet não disponível")
    
    user = db.query(User).filter(User.id == adopt_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    pet.status = "adopted"
    pet.adopted_by = adopt_data.user_id
    pet.adopted_at = datetime.utcnow()
    
    db.commit()
    db.refresh(pet)
    return pet

@app.get("/users", tags=["Usuários"])
async def list_users(db: Session = Depends(get_db)):
    """
    Listar todos os usuários
    """
    users = db.query(User).all()
    return {"users": users}

@app.post("/users", status_code=201, tags=["Usuários"])
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):

    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email já existe")
    
    user = User(**user_data.dict())
    user.created_at = datetime.utcnow()
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.get("/users/{user_id}", tags=["Usuários"])
async def get_user(user_id: int, db: Session = Depends(get_db)):
   
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
