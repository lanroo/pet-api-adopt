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
from schemas import PetCreate, PetUpdate, UserCreate, UserUpdate, AdoptRequest, PetResponse, PetFilter
from utils import get_species_label, get_gender_label, get_status_label
from app_types import GenderEnum, SpeciesEnum, StatusEnum
from app_types.constants import UPLOAD_DIR, MAX_PAGE_SIZE, MIN_PAGE_SIZE

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

os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.on_event("startup")
async def startup_event():
    """Inicializar banco de dados na startup"""
    try:
        init_db()
        print("✅ Banco de dados inicializado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao inicializar banco: {e}")


@app.get("/", tags=["Sistema"])
async def root():
    """
    Página inicial da API
    """
    return {
        "message": "Pet Adoption API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "pets": "/pets",
        "users": "/users"
    }

@app.get("/health", tags=["Sistema"])
async def health_check():
    """
    Verificar se a API está funcionando
    """
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.get("/pets", response_model=List[PetResponse], tags=["Pets"])
async def list_pets(
    species: Optional[SpeciesEnum] = Query(None, description="Filtrar por espécie"),
    gender: Optional[GenderEnum] = Query(None, description="Filtrar por gênero"),
    city: Optional[str] = Query(None, description="Filtrar por cidade"),
    status: Optional[StatusEnum] = Query(None, description="Filtrar por status"),
    min_age: Optional[float] = Query(None, description="Idade mínima em meses"),
    max_age: Optional[float] = Query(None, description="Idade máxima em meses"),
    skip: int = Query(0, ge=0),
    limit: int = Query(MAX_PAGE_SIZE, ge=MIN_PAGE_SIZE, le=MAX_PAGE_SIZE),
    db: Session = Depends(get_db)
):
    """
    Buscar pets com filtros opcionais
    
    - **species**: dog, cat
    - **gender**: male, female
    - **city**: qualquer cidade
    - **status**: available, adopted, pending
    - **min_age**: idade mínima em meses
    - **max_age**: idade máxima em meses
    - **skip**: número de registros para pular
    - **limit**: máximo 100 itens por página
    """
    query = db.query(Pet)
    
    if species:
        query = query.filter(Pet.species == species)
    
    if gender:
        query = query.filter(Pet.gender == gender)
    
    if city:
        query = query.filter(Pet.city.ilike(f"%{city}%"))
    
    if status:
        query = query.filter(Pet.status == status)
    
    if min_age is not None:
        query = query.filter(Pet.age >= min_age)
    
    if max_age is not None:
        query = query.filter(Pet.age <= max_age)
    
    pets = query.offset(skip).limit(limit).all()
    return pets

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

@app.get("/pets/{pet_id}", response_model=PetResponse, tags=["Pets"])
async def get_pet(pet_id: int, db: Session = Depends(get_db)):
    """
    Buscar pet por ID
    """
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    return pet

@app.post("/pets", response_model=PetResponse, status_code=201, tags=["Pets"])
async def create_pet(pet_data: PetCreate, db: Session = Depends(get_db)):
    """
    Criar novo pet
    
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
    pet = Pet(**pet_data.model_dump())
    db.add(pet)
    db.commit()
    db.refresh(pet)
    return pet

@app.put("/pets/{pet_id}", response_model=PetResponse, tags=["Pets"])
async def update_pet(pet_id: int, pet_data: PetUpdate, db: Session = Depends(get_db)):
    """
    Atualizar pet existente
    """
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    
    update_data = pet_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(pet, field, value)
    
    db.commit()
    db.refresh(pet)
    return pet

@app.delete("/pets/{pet_id}", tags=["Pets"])
async def delete_pet(pet_id: int, db: Session = Depends(get_db)):
    """
    Deletar pet
    """
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    
    db.delete(pet)
    db.commit()
    return {"message": "Pet deletado com sucesso"}


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

@app.post("/pets/{pet_id}/photos", tags=["Pets"])
async def upload_pet_photos(
    pet_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload fotos para um pet específico
    """
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    
    uploaded_files = []
    
    for file in files:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail=f"Arquivo {file.filename} não é uma imagem")
        
        # Gerar nome único para o arquivo
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # Salvar arquivo
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        uploaded_files.append(unique_filename)
    
    # Atualizar lista de fotos do pet
    if pet.photos is None:
        pet.photos = []
    
    pet.photos.extend(uploaded_files)
    pet.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(pet)
    
    return {
        "message": f"{len(uploaded_files)} foto(s) enviada(s) com sucesso",
        "pet_id": pet_id,
        "uploaded_files": uploaded_files,
        "total_photos": len(pet.photos)
    }

@app.get("/pets/filters/options", tags=["Pets"])
async def get_filter_options(db: Session = Depends(get_db)):
    """
    Obter opções disponíveis para filtros
    """
    cities = db.query(Pet.city).distinct().filter(Pet.city.isnot(None)).all()
    cities = [city[0] for city in cities if city[0]]
    
    return {
        "species": [{"value": species.value, "label": get_species_label(species)} for species in SpeciesEnum],
        "genders": [{"value": gender.value, "label": get_gender_label(gender)} for gender in GenderEnum],
        "cities": sorted(cities),
        "status": [{"value": status.value, "label": get_status_label(status)} for status in StatusEnum]
    }

@app.get("/uploads/{filename}", tags=["Arquivos"])
async def get_uploaded_file(filename: str):
    """
    Servir arquivos de upload (fotos dos pets)
    """
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    
    from fastapi.responses import FileResponse
    return FileResponse(file_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
