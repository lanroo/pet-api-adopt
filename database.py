from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from app_types.constants import DATABASE_URL
from auth import get_password_hash

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    from models import Base, Pet, User
    from app_types import GenderEnum, SpeciesEnum, StatusEnum
    
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Verificar se já existem dados (pets ou usuários)
        if db.query(Pet).count() > 0 and db.query(User).count() > 0:
            return
        
        user1 = User(
            full_name="João Silva",
            email="joao@email.com",
            phone="11999999999",
            city="São Paulo",
            password=get_password_hash("senha123")
        )
        
        user2 = User(
            full_name="Maria Santos",
            email="maria@email.com",
            phone="21999999999",
            city="Rio de Janeiro",
            password=get_password_hash("senha123")
        )
        
        # Usuário admin
        admin_user = User(
            full_name="Admin",
            email="yladacz@gmail.com",
            phone="11999999999",
            city="São Paulo",
            password=get_password_hash("@Senha123")
        )
        
        db.add(user1)
        db.add(user2)
        db.add(admin_user)
        db.commit()
        
        # Dados atualizados com gêneros corretos
        dogs_data = [
            {"name": "Luna", "gender": GenderEnum.FEMALE, "photo": "https://images.unsplash.com/photo-1552053831-71594a27632d?w=400&h=300&fit=crop"},
            {"name": "Max", "gender": GenderEnum.MALE, "photo": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=400&h=300&fit=crop"},
            {"name": "Bella", "gender": GenderEnum.FEMALE, "photo": "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=400&h=300&fit=crop"},
            {"name": "Thor", "gender": GenderEnum.MALE, "photo": "https://images.unsplash.com/photo-1551717743-49959800b1f6?w=400&h=300&fit=crop"},
            {"name": "Lola", "gender": GenderEnum.FEMALE, "photo": "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=400&h=300&fit=crop"},
            {"name": "Zeus", "gender": GenderEnum.MALE, "photo": "https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=400&h=300&fit=crop"},
            {"name": "Maya", "gender": GenderEnum.FEMALE, "photo": "https://images.unsplash.com/photo-1605568427561-40dd23c2acea?w=400&h=300&fit=crop"},
            {"name": "Apollo", "gender": GenderEnum.MALE, "photo": "https://www.petelegante.com.br/media/dicas/ado%C3%A7%C3%A3o-de-cachorro-filhote.jpg"},
            {"name": "Nala", "gender": GenderEnum.FEMALE, "photo": "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=400&h=300&fit=crop"},
            {"name": "Rocky", "gender": GenderEnum.MALE, "photo": "https://static.wixstatic.com/media/e2e4ef_8681efaf6b4c4f05b2605a1162957150~mv2.jpg/v1/fill/w_516,h_432,al_c,q_80,usm_0.66_1.00_0.01,enc_avif,quality_auto/Simon_cachorro_PatinhasCarentes_05.jpg"},
            {"name": "Sofia", "gender": GenderEnum.FEMALE, "photo": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=400&h=300&fit=crop"},
            {"name": "Bruno", "gender": GenderEnum.MALE, "photo": "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=400&h=300&fit=crop"},
            {"name": "Rex", "gender": GenderEnum.MALE, "photo": "https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=400&h=300&fit=crop"},
            {"name": "Karen", "gender": GenderEnum.FEMALE, "photo": "https://images.unsplash.com/photo-1605568427561-40dd23c2acea?w=400&h=300&fit=crop"},
            {"name": "Charlie", "gender": GenderEnum.MALE, "photo": "https://images.unsplash.com/photo-1551717743-49959800b1f6?w=400&h=300&fit=crop"}
        ]
        
        cats_data = [
            {"name": "Mimi", "gender": GenderEnum.FEMALE, "photo": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400&h=300&fit=crop"},
            {"name": "Simba", "gender": GenderEnum.MALE, "photo": "https://images.unsplash.com/photo-1574158622682-e40e69881006?w=400&h=300&fit=crop"},
            {"name": "Carminha", "gender": GenderEnum.FEMALE, "photo": "https://images.unsplash.com/photo-1596854407944-bf87f6fdd49e?w=400&h=300&fit=crop"},
            {"name": "Felix", "gender": GenderEnum.MALE, "photo": "https://images.unsplash.com/photo-1573865526739-10659fec78a5?w=400&h=300&fit=crop"},
            {"name": "BellaCat", "gender": GenderEnum.FEMALE, "photo": "https://images.unsplash.com/photo-1513245543132-31f507417b26?w=400&h=300&fit=crop"},
            {"name": "Garfield", "gender": GenderEnum.MALE, "photo": "https://images.unsplash.com/photo-1592194996308-7b43878e84a6?w=400&h=300&fit=crop"},
            {"name": "NalaCat", "gender": GenderEnum.FEMALE, "photo": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400&h=300&fit=crop"},
            {"name": "Pink", "gender": GenderEnum.MALE, "photo": "https://images.unsplash.com/photo-1574158622682-e40e69881006?w=400&h=300&fit=crop"},
            {"name": "MayaCat", "gender": GenderEnum.FEMALE, "photo": "https://images.unsplash.com/photo-1596854407944-bf87f6fdd49e?w=400&h=300&fit=crop"},
            {"name": "Whiskers", "gender": GenderEnum.MALE, "photo": "https://images.unsplash.com/photo-1573865526739-10659fec78a5?w=400&h=300&fit=crop"},
            {"name": "Laly", "gender": GenderEnum.FEMALE, "photo": "https://images.unsplash.com/photo-1513245543132-31f507417b26?w=400&h=300&fit=crop"},
            {"name": "Shadow", "gender": GenderEnum.MALE, "photo": "https://images.unsplash.com/photo-1592194996308-7b43878e84a6?w=400&h=300&fit=crop"},
            {"name": "Brina", "gender": GenderEnum.FEMALE, "photo": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400&h=300&fit=crop"},
            {"name": "Tiger", "gender": GenderEnum.MALE, "photo": "https://images.unsplash.com/photo-1574158622682-e40e69881006?w=400&h=300&fit=crop"},
            {"name": "Mia", "gender": GenderEnum.FEMALE, "photo": "https://images.unsplash.com/photo-1596854407944-bf87f6fdd49e?w=400&h=300&fit=crop"}
        ]
        
        cities = ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Salvador", "Brasília", "Fortaleza", "Manaus", "Curitiba", "Recife", "Porto Alegre"]
        
        # Criar cachorros
        for i, dog in enumerate(dogs_data):
            pet = Pet(
                name=dog["name"],
                species=SpeciesEnum.DOG,
                breed="Vira-lata",
                age=12 + (i * 6),  # 1-4 anos em meses
                gender=dog["gender"],
                city=cities[i % len(cities)],
                description=f"{dog['name']} é um{'a' if dog['gender'] == GenderEnum.FEMALE else ''} cachorro{'a' if dog['gender'] == GenderEnum.FEMALE else ''} muito carinhoso{'a' if dog['gender'] == GenderEnum.FEMALE else ''} e brincalhão{'a' if dog['gender'] == GenderEnum.FEMALE else ''}.",
                photos=[dog["photo"]],
                status=StatusEnum.AVAILABLE
            )
            db.add(pet)
        
        # Criar gatos
        for i, cat in enumerate(cats_data):
            pet = Pet(
                name=cat["name"],
                species=SpeciesEnum.CAT,
                breed="Sem raça definida",
                age=8 + (i * 4),  # 8 meses - 2 anos
                gender=cat["gender"],
                city=cities[i % len(cities)],
                description=f"{cat['name']} é um{'a' if cat['gender'] == GenderEnum.FEMALE else ''} gato{'a' if cat['gender'] == GenderEnum.FEMALE else ''} muito dócil e independente.",
                photos=[cat["photo"]],
                status=StatusEnum.AVAILABLE
            )
            db.add(pet)
        
        db.commit()
        print("✅ Dados criados com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()