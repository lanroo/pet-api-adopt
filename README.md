# 🐾 Pet Adoption API

API para sistema de adoção de pets com FastAPI.

## 🚀 Instalação Rápida (Sem Docker)

### Método 1: Script Automático (Recomendado)
```bash
cd pet-adoption-api
./start.sh
```

### Método 2: Manual
```bash
cd pet-adoption-api

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install fastapi "uvicorn[standard]" sqlalchemy "pydantic[email]" python-multipart python-dotenv

# Inicializar banco
python database.py

# Iniciar servidor
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Docker (Alternativo)
```bash
cd pet-adoption-api
docker-compose up -d
```

## 📚 Endpoints

- `GET /pets` - Listar pets
- `POST /pets` - Criar pet  
- `GET /pets/{id}` - Pet específico
- `GET /pets/search?q=termo` - Buscar
- `POST /pets/{id}/adopt` - Adotar
- `GET /pets/stats` - Estatísticas
- `POST /users` - Criar usuário

## 🌐 Acessos

- **API**: http://localhost:8000
- **Documentação Swagger**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **pgAdmin** (Docker): http://localhost:5050

## 🧪 Teste Rápido

```bash
# Listar pets
curl http://localhost:8000/pets

# Criar usuário
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d '{"full_name": "João", "email": "joao@test.com", "phone": "11999999999", "city": "São Paulo"}'

# Ver stats
curl http://localhost:8000/pets/stats
```

Acesse http://localhost:8000/docs para documentação completa!
