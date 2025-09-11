from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Configuração simples do banco
DATABASE_URL = "sqlite:///./pet_adoption.db"

# Engine simples
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
    from datetime import datetime
    
    # Criar tabelas
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Verificar se já existem pets
        if db.query(Pet).count() > 0:
            return
        
        # Criar usuários
        user1 = User(
            full_name="João Silva",
            email="joao@email.com",
            phone="11999999999",
            city="São Paulo"
        )
        
        user2 = User(
            full_name="Maria Santos",
            email="maria@email.com",
            phone="21999999999",
            city="Rio de Janeiro"
        )
        
        db.add(user1)
        db.add(user2)
        db.commit()
        
        # Criar pets
        cities = ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Salvador", "Brasília", "Fortaleza", "Manaus", "Curitiba", "Recife", "Porto Alegre"]
        
        # Cães com nomes e fotos específicas
        dogs_data = [
            {"name": "Luna", "photo": "https://images.unsplash.com/photo-1552053831-71594a27632d?w=400&h=300&fit=crop"},
            {"name": "Max", "photo": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=400&h=300&fit=crop"},
            {"name": "Bella", "photo": "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=400&h=300&fit=crop"},
            {"name": "Thor", "photo": "https://images.unsplash.com/photo-1551717743-49959800b1f6?w=400&h=300&fit=crop"},
            {"name": "Lola", "photo": "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=400&h=300&fit=crop"},
            {"name": "Zeus", "photo": "https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=400&h=300&fit=crop"},
            {"name": "Maya", "photo": "https://images.unsplash.com/photo-1605568427561-40dd23c2acea?w=400&h=300&fit=crop"},
            {"name": "Apollo", "photo": "https://www.petelegante.com.br/media/dicas/ado%C3%A7%C3%A3o-de-cachorro-filhote.jpg"},
            {"name": "Nala", "photo": "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=400&h=300&fit=crop"},
            {"name": "Rocky", "photo": "https://static.wixstatic.com/media/e2e4ef_8681efaf6b4c4f05b2605a1162957150~mv2.jpg/v1/fill/w_516,h_432,al_c,q_80,usm_0.66_1.00_0.01,enc_avif,quality_auto/Simon_cachorro_PatinhasCarentes_05.jpg"},
            {"name": "Sofia", "photo": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=400&h=300&fit=crop"},
            {"name": "Bruno", "photo": "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=400&h=300&fit=crop"},
            {"name": "Rex", "photo": "https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=400&h=300&fit=crop"},
            {"name": "Mia", "photo": "https://images.unsplash.com/photo-1605568427561-40dd23c2acea?w=400&h=300&fit=crop"},
            {"name": "Charlie", "photo": "https://images.unsplash.com/photo-1551717743-49959800b1f6?w=400&h=300&fit=crop"}
        ]
        
        for i, dog in enumerate(dogs_data):
            pet = Pet(
                name=dog["name"],
                species="dog",
                breed="Cachorro",  # Raça genérica
                age=12 + (i * 2),
                gender="female" if i % 2 == 0 else "male",
                city=cities[i % len(cities)],
                description=f"Cachorro muito carinhoso e brincalhão",
                photos=[dog["photo"]]  # Foto específica para cada pet
            )
            db.add(pet)
        
        # Gatos com nomes e fotos específicas
        cats_data = [
            {"name": "Mimi", "photo": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400&h=300&fit=crop"},
            {"name": "Simba", "photo": "https://images.unsplash.com/photo-1574158622682-e40e69881006?w=400&h=300&fit=crop"},
            {"name": "Luna", "photo": "https://images.unsplash.com/photo-1596854407944-bf87f6fdd49e?w=400&h=300&fit=crop"},
            {"name": "Felix", "photo": "https://images.unsplash.com/photo-1573865526739-10659fec78a5?w=400&h=300&fit=crop"},
            {"name": "Bella", "photo": "https://images.unsplash.com/photo-1513245543132-31f507417b26?w=400&h=300&fit=crop"},
            {"name": "Garfield", "photo": "https://images.unsplash.com/photo-1592194996308-7b43878e84a6?w=400&h=300&fit=crop"},
            {"name": "Nala", "photo": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400&h=300&fit=crop"},
            {"name": "Tom", "photo": "https://images.unsplash.com/photo-1574158622682-e40e69881006?w=400&h=300&fit=crop"},
            {"name": "Maya", "photo": "https://images.unsplash.com/photo-1596854407944-bf87f6fdd49e?w=400&h=300&fit=crop"},
            {"name": "Whiskers", "photo": "https://images.unsplash.com/photo-1573865526739-10659fec78a5?w=400&h=300&fit=crop"},
            {"name": "Sofia", "photo": "https://images.unsplash.com/photo-1513245543132-31f507417b26?w=400&h=300&fit=crop"},
            {"name": "Shadow", "photo": "https://images.unsplash.com/photo-1592194996308-7b43878e84a6?w=400&h=300&fit=crop"},
            {"name": "Lola", "photo": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400&h=300&fit=crop"},
            {"name": "Tiger", "photo": "https://images.unsplash.com/photo-1574158622682-e40e69881006?w=400&h=300&fit=crop"},
            {"name": "Mia", "photo": "https://images.unsplash.com/photo-1596854407944-bf87f6fdd49e?w=400&h=300&fit=crop"}
        ]
        
        for i, cat in enumerate(cats_data):
            pet = Pet(
                name=cat["name"],
                species="cat",
                breed="Gato",  # Raça genérica
                age=8 + (i * 1.5),
                gender="male" if i % 2 == 0 else "female",
                city=cities[(i + 5) % len(cities)],
                description=f"Gato muito dócil e independente",
                photos=[cat["photo"]]  # Foto específica para cada pet
            )
            db.add(pet)
        
        db.commit()
        print("✅ Dados criados com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()