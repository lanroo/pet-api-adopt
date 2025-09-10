from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./pet_adoption.db"
)

if "vercel" in DATABASE_URL or os.getenv("VERCEL"):
    DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(DATABASE_URL)
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
    
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        if db.query(User).count() > 0:
            print("✅ Banco já tem dados!")
            return
        
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
            
       
        cities = ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Salvador", "Brasília", "Fortaleza", "Manaus", "Curitiba", "Recife", "Porto Alegre"]
        dog_breeds = ["Golden Retriever", "Pastor Alemão", "Labrador", "Bulldog", "Poodle", "Beagle", "Rottweiler", "Husky", "Dachshund", "Boxer", "Chihuahua", "Shih Tzu", "Border Collie", "Doberman", "Maltês"]
        cat_breeds = ["Persa", "Siamês", "Maine Coon", "Ragdoll", "British Shorthair", "Abissínio", "Birmanês", "Sphynx", "Scottish Fold", "Angorá", "Bombay", "Manx", "Oriental", "Siberiano", "Devon Rex"]
        
        
        dog_names = ["Luna", "Max", "Bella", "Thor", "Lola", "Zeus", "Maya", "Apollo", "Nala", "Rocky", "Sofia", "Bruno", "Rex", "Mia", "Charlie"]
        for i in range(15):
            pet = Pet(
                name=dog_names[i],
                species="dog",
                breed=dog_breeds[i],
                age=12 + (i * 2),  
                gender="female" if i % 2 == 0 else "male",
                city=cities[i % len(cities)],
                description=f"Cachorro {dog_breeds[i].lower()} muito carinhoso e brincalhão"
            )
            db.add(pet)
        
        cat_names = ["Mimi", "Simba", "Luna", "Felix", "Bella", "Garfield", "Nala", "Tom", "Maya", "Whiskers", "Sofia", "Shadow", "Lola", "Tiger", "Mia"]
        for i in range(15):
            pet = Pet(
                name=cat_names[i],
                species="cat",
                breed=cat_breeds[i],
                age=8 + (i * 1.5),  
                gender="male" if i % 2 == 0 else "female",
                city=cities[(i + 5) % len(cities)],  
                description=f"Gato {cat_breeds[i].lower()} muito dócil e independente"
            )
            db.add(pet)
        db.commit()
        
        print("✅ Dados de exemplo criados!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
