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
        dog_breeds = ["Golden Retriever", "Pastor Alemão", "Labrador", "Bulldog", "Poodle", "Beagle", "Rottweiler", "Husky", "Dachshund", "Boxer", "Chihuahua", "Shih Tzu", "Border Collie", "Doberman", "Maltês"]
        cat_breeds = ["Persa", "Siamês", "Maine Coon", "Ragdoll", "British Shorthair", "Abissínio", "Birmanês", "Sphynx", "Scottish Fold", "Angorá", "Bombay", "Manx", "Oriental", "Siberiano", "Devon Rex"]
        
        dog_names = ["Luna", "Max", "Bella", "Thor", "Lola", "Zeus", "Maya", "Apollo", "Nala", "Rocky", "Sofia", "Bruno", "Rex", "Mia", "Charlie"]
        dog_photos = [
            "https://images.unsplash.com/photo-1552053831-71594a27632d?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1551717743-49959800b1f6?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1551717743-49959800b1f6?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1605568427561-40dd23c2acea?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1552053831-71594a27632d?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1605568427561-40dd23c2acea?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1551717743-49959800b1f6?w=400&h=300&fit=crop"
        ]
        
        for i in range(15):
            pet = Pet(
                name=dog_names[i],
                species="dog",
                breed=dog_breeds[i],
                age=12 + (i * 2),
                gender="female" if i % 2 == 0 else "male",
                city=cities[i % len(cities)],
                description=f"Cachorro {dog_breeds[i].lower()} muito carinhoso e brincalhão",
                photos=[dog_photos[i]]  # Usar URLs de imagens reais
            )
            db.add(pet)
        
        cat_names = ["Mimi", "Simba", "Luna", "Felix", "Bella", "Garfield", "Nala", "Tom", "Maya", "Whiskers", "Sofia", "Shadow", "Lola", "Tiger", "Mia"]
        cat_photos = [
            "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1574158622682-e40e69881006?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1596854407944-bf87f6fdd49e?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1573865526739-10659fec78a5?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1513245543132-31f507417b26?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1592194996308-7b43878e84a6?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1574158622682-e40e69881006?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1596854407944-bf87f6fdd49e?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1573865526739-10659fec78a5?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1513245543132-31f507417b26?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1592194996308-7b43878e84a6?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1574158622682-e40e69881006?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1596854407944-bf87f6fdd49e?w=400&h=300&fit=crop"
        ]
        
        for i in range(15):
            pet = Pet(
                name=cat_names[i],
                species="cat",
                breed=cat_breeds[i],
                age=8 + (i * 1.5),
                gender="male" if i % 2 == 0 else "female",
                city=cities[(i + 5) % len(cities)],
                description=f"Gato {cat_breeds[i].lower()} muito dócil e independente",
                photos=[cat_photos[i]]  # Usar URLs de imagens reais
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