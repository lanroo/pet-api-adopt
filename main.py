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
from models import Pet, User, Base, AdoptionRequest
from schemas import (
    PetCreate, PetUpdate, UserCreate, UserUpdate, AdoptRequest, PetResponse, PetFilter, PetListResponse,
    AdoptionRequestCreate, AdoptionRequestUpdate, AdoptionRequestResponse, AdoptionRequestListResponse,
    UserLogin, UserRegister, Token, UserProfile
)
from auth import verify_password, get_password_hash, create_access_token, check_dependencies
from auth_deps import get_current_user, get_current_user_optional
from utils import get_species_label, get_gender_label, get_status_label
from app_types import GenderEnum, SpeciesEnum, StatusEnum, AdoptionStatusEnum
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

_db_initialized = False

def ensure_db_initialized():
    """Garantir que o banco está inicializado"""
    global _db_initialized
    if not _db_initialized:
        try:
            init_db()
            _db_initialized = True
            print("✅ Banco de dados inicializado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao inicializar banco: {e}")
            # Continuar mesmo com erro


@app.get("/", tags=["Sistema"])
async def root():
    """
    Página inicial da API
    """
    # Inicializar banco na primeira requisição
    ensure_db_initialized()
    
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
    # Inicializar banco na primeira requisição
    ensure_db_initialized()
    
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.post("/init-db", tags=["Sistema"])
async def initialize_database():
    """
    Inicializar banco de dados manualmente
    """
    try:
        init_db()
        return {"message": "Banco de dados inicializado com sucesso!"}
    except Exception as e:
        return {"error": f"Erro ao inicializar banco: {str(e)}"}

@app.get("/debug/db-status", tags=["Sistema"])
async def debug_database_status():
    """
    Debug: Verificar status do banco de dados
    """
    try:
        from models import Pet, User
        db = next(get_db())
        
        pets_count = db.query(Pet).count()
        users_count = db.query(User).count()
        
        # Listar usuários
        users = db.query(User).all()
        users_data = []
        for user in users:
            users_data.append({
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "has_password": bool(user.password)
            })
        
        return {
            "pets_count": pets_count,
            "users_count": users_count,
            "users": users_data
        }
    except Exception as e:
        return {"error": f"Erro ao verificar banco: {str(e)}"}

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
    # Transformar os dados para incluir o campo whatsapp
    users_data = []
    for user in users:
        user_dict = {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "whatsapp": user.whatsapp,
            "city": user.city,
            "created_at": user.created_at
        }
        users_data.append(user_dict)
    return {"users": users_data}

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
    
    # Transformar os dados para incluir o campo whatsapp
    user_dict = {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "whatsapp": user.whatsapp,
        "city": user.city,
        "created_at": user.created_at
    }
    return user_dict

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

# AUTHENTICATION ENDPOINTS

@app.post("/api/auth/register", response_model=UserProfile, status_code=201, tags=["Autenticação"])
async def register_user(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Registrar novo usuário
    """
    # Verificar se as dependências estão instaladas
    if not check_dependencies():
        raise HTTPException(
            status_code=500, 
            detail="Dependências de autenticação não instaladas. Execute: pip install passlib python-jose"
        )
    
    # Verificar se email já existe
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400, 
            detail="Email já cadastrado"
        )
    
    # Criar hash da senha
    hashed_password = get_password_hash(user_data.password)
    
    # Criar usuário
    user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        password=hashed_password,
        whatsapp=user_data.whatsapp,
        city=user_data.city
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


@app.post("/api/auth/login", response_model=Token, tags=["Autenticação"])
async def login_user(login_data: UserLogin, db: Session = Depends(get_db)):
    """
    Fazer login com email ou nome de usuário
    """
    # Verificar se as dependências estão instaladas
    if not check_dependencies():
        raise HTTPException(
            status_code=500, 
            detail="Dependências de autenticação não instaladas. Execute: pip install passlib python-jose"
        )
    
    # Buscar usuário por email ou nome
    user = db.query(User).filter(
        (User.email == login_data.username) | 
        (User.full_name.ilike(f"%{login_data.username}%"))
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=401, 
            detail="Usuário ou senha incorretos"
        )
    
    # Verificar senha
    if not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=401, 
            detail="Usuário ou senha incorretos"
        )
    
    # Criar token
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.get("/user/login", tags=["Autenticação"])
async def login_user_legacy(username: str, password: str, db: Session = Depends(get_db)):
    """
    Login legado - compatível com frontend atual
    """
    # Verificar se as dependências estão instaladas
    if not check_dependencies():
        raise HTTPException(
            status_code=500, 
            detail="Dependências de autenticação não instaladas"
        )
    
    # Buscar usuário por email ou nome
    user = db.query(User).filter(
        (User.email == username) | 
        (User.full_name.ilike(f"%{username}%"))
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=401, 
            detail="Usuário ou senha incorretos"
        )
    
    # Verificar senha
    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=401, 
            detail="Usuário ou senha incorretos"
        )
    
    # Criar token
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "whatsapp": user.whatsapp,
            "city": user.city
        }
    }


@app.get("/api/auth/me", response_model=UserProfile, tags=["Autenticação"])
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """
    Obter dados do usuário logado
    """
    return current_user


@app.post("/api/auth/logout", tags=["Autenticação"])
async def logout_user():
    """
    Fazer logout (no JWT, o logout é feito no frontend removendo o token)
    """
    return {"message": "Logout realizado com sucesso. Remova o token do frontend."}

# ============================================================================
# ENDPOINTS DE ADOÇÃO
# ============================================================================

@app.post("/adoption-requests", response_model=AdoptionRequestResponse, tags=["Adoções"])
async def create_adoption_request(
    adoption_request: AdoptionRequestCreate,
    db: Session = Depends(get_db)
):
    """
    Criar novo pedido de adoção
    """
    try:
        # Criar o pedido de adoção
        db_adoption = AdoptionRequest(**adoption_request.dict())
        db.add(db_adoption)
        db.commit()
        db.refresh(db_adoption)
        
        return db_adoption
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar pedido de adoção: {str(e)}")

@app.get("/adoption-requests", response_model=List[AdoptionRequestResponse], tags=["Adoções"])
async def get_adoption_requests(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=100, description="Número máximo de registros"),
    status: Optional[AdoptionStatusEnum] = Query(None, description="Filtrar por status"),
    db: Session = Depends(get_db)
):
    """
    Listar todos os pedidos de adoção
    """
    query = db.query(AdoptionRequest)
    
    if status:
        query = query.filter(AdoptionRequest.status == status)
    
    return query.offset(skip).limit(limit).all()

@app.get("/adoption-requests/{adoption_id}", response_model=AdoptionRequestResponse, tags=["Adoções"])
async def get_adoption_request(
    adoption_id: int,
    db: Session = Depends(get_db)
):
    """
    Buscar pedido de adoção específico
    """
    adoption = db.query(AdoptionRequest).filter(AdoptionRequest.id == adoption_id).first()
    if not adoption:
        raise HTTPException(status_code=404, detail="Pedido de adoção não encontrado")
    return adoption

@app.put("/adoption-requests/{adoption_id}", response_model=AdoptionRequestResponse, tags=["Adoções"])
async def update_adoption_request(
    adoption_id: int,
    adoption_update: AdoptionRequestUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualizar pedido de adoção
    """
    adoption = db.query(AdoptionRequest).filter(AdoptionRequest.id == adoption_id).first()
    if not adoption:
        raise HTTPException(status_code=404, detail="Pedido de adoção não encontrado")
    
    # Atualizar apenas os campos fornecidos
    update_data = adoption_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(adoption, key, value)
    
    db.commit()
    db.refresh(adoption)
    return adoption

@app.delete("/adoption-requests/{adoption_id}", tags=["Adoções"])
async def delete_adoption_request(
    adoption_id: int,
    db: Session = Depends(get_db)
):
    """
    Deletar pedido de adoção
    """
    adoption = db.query(AdoptionRequest).filter(AdoptionRequest.id == adoption_id).first()
    if not adoption:
        raise HTTPException(status_code=404, detail="Pedido de adoção não encontrado")
    
    db.delete(adoption)
    db.commit()
    return {"message": "Pedido de adoção deletado com sucesso"}

@app.get("/adoption-requests/count", tags=["Adoções"])
async def get_adoption_requests_count(
    status: Optional[AdoptionStatusEnum] = Query(None, description="Filtrar por status"),
    db: Session = Depends(get_db)
):
    """
    Contar pedidos de adoção
    """
    query = db.query(AdoptionRequest)
    
    if status:
        total = query.filter(AdoptionRequest.status == status).count()
        return {"count": total}
    else:
        total = query.count()
        pending = query.filter(AdoptionRequest.status == AdoptionStatusEnum.PENDING).count()
        approved = query.filter(AdoptionRequest.status == AdoptionStatusEnum.APPROVED).count()
        rejected = query.filter(AdoptionRequest.status == AdoptionStatusEnum.REJECTED).count()
        completed = query.filter(AdoptionRequest.status == AdoptionStatusEnum.COMPLETED).count()
        
        return {
            "total": total,
            "pending": pending,
            "approved": approved,
            "rejected": rejected,
            "completed": completed
        }

@app.delete("/users/{user_id}", tags=["Usuários"])
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Deletar usuário específico
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        db.delete(user)
        db.commit()
        return {"message": f"Usuário {user.full_name} deletado com sucesso"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar usuário: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
