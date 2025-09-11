# 🚀 Pet Adoption API - Endpoints Completos

## 📍 URL da API
```
https://projeto-jornadadados-pet-api-adoptt.zjnxkg.easypanel.host
```

## 📖 Documentação Swagger
```
https://projeto-jornadadados-pet-api-adoptt.zjnxkg.easypanel.host/docs
```

---

## 🏠 SISTEMA

### Informações da API
```http
GET /
```
**Resposta:**
```json
{
  "message": "Pet Adoption API",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/health",
  "pets": "/pets",
  "users": "/users"
}
```

### Status da API
```http
GET /health
```
**Resposta:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-11T01:30:00"
}
```

---

## 🐕🐱 PETS

### Listar todos os pets (com filtros)
```http
GET /pets?species=dog&city=São Paulo&status=available&page=1&limit=10
```

**Parâmetros de Query:**
- `species` (opcional): `dog` ou `cat`
- `city` (opcional): qualquer cidade
- `status` (opcional): `available` ou `adopted`
- `page` (opcional): número da página (padrão: 1)
- `limit` (opcional): itens por página (padrão: 10, máximo: 100)

**Resposta:**
```json
{
  "pets": [
    {
      "id": 1,
      "name": "Luna",
      "species": "dog",
      "breed": "Cachorro",
      "age": 12,
      "gender": "female",
      "city": "São Paulo",
      "description": "Cachorro muito carinhoso e brincalhão",
      "photos": ["https://images.unsplash.com/photo-1552053831-71594a27632d?w=400&h=300&fit=crop"],
      "status": "available",
      "created_at": "2025-01-11T01:30:00",
      "updated_at": "2025-01-11T01:30:00"
    }
  ],
  "total": 30,
  "page": 1,
  "limit": 10
}
```

### Buscar pets por texto
```http
GET /pets/search?q=luna
```

**Resposta:**
```json
{
  "pets": [...],
  "query": "luna"
}
```

### Buscar pet específico
```http
GET /pets/{pet_id}
```

**Resposta:**
```json
{
  "id": 1,
  "name": "Luna",
  "species": "dog",
  "breed": "Cachorro",
  "age": 12,
  "gender": "female",
  "city": "São Paulo",
  "description": "Cachorro muito carinhoso e brincalhão",
  "photos": ["https://images.unsplash.com/photo-1552053831-71594a27632d?w=400&h=300&fit=crop"],
  "status": "available",
  "created_at": "2025-01-11T01:30:00",
  "updated_at": "2025-01-11T01:30:00"
}
```

### Criar novo pet
```http
POST /pets
```

**Body:**
```json
{
  "name": "Luna",
  "species": "dog",
  "breed": "Cachorro",
  "age": 24,
  "gender": "female",
  "city": "São Paulo",
  "description": "Cadela muito carinhosa"
}
```

**Resposta:** Pet criado (status 201)

### Atualizar pet
```http
PUT /pets/{pet_id}
```

**Body:**
```json
{
  "name": "Luna Atualizada",
  "description": "Nova descrição"
}
```

**Resposta:** Pet atualizado

### Deletar pet
```http
DELETE /pets/{pet_id}
```

**Resposta:** 204 (sem conteúdo)

### Upload de fotos
```http
POST /pets/{pet_id}/photos
```

**Body:** FormData com arquivos de imagem

**Resposta:**
```json
{
  "message": "2 foto(s) enviada(s) com sucesso",
  "pet_id": 1,
  "uploaded_files": ["uuid1.jpg", "uuid2.jpg"],
  "total_photos": 3
}
```

---

## 👥 USUÁRIOS

### Listar usuários
```http
GET /users
```

**Resposta:**
```json
{
  "users": [
    {
      "id": 1,
      "full_name": "João Silva",
      "email": "joao@email.com",
      "phone": "11999999999",
      "city": "São Paulo",
      "created_at": "2025-01-11T01:30:00"
    }
  ]
}
```

### Criar usuário
```http
POST /users
```

**Body:**
```json
{
  "full_name": "João Silva",
  "email": "joao@email.com",
  "phone": "11999999999",
  "city": "São Paulo"
}
```

**Resposta:** Usuário criado (status 201)

### Buscar usuário específico
```http
GET /users/{user_id}
```

**Resposta:**
```json
{
  "id": 1,
  "full_name": "João Silva",
  "email": "joao@email.com",
  "phone": "11999999999",
  "city": "São Paulo",
  "created_at": "2025-01-11T01:30:00"
}
```

---

## 💝 ADOÇÃO

### Adotar pet
```http
POST /pets/{pet_id}/adopt
```

**Body:**
```json
{
  "user_id": 1
}
```

**Resposta:** Pet atualizado com status "adopted"

---

## 📊 ESTATÍSTICAS

### Estatísticas dos pets
```http
GET /pets/stats
```

**Resposta:**
```json
{
  "total_pets": 30,
  "available_pets": 25,
  "adopted_pets": 5
}
```

---

## 📁 ARQUIVOS

### Servir arquivos de upload
```http
GET /uploads/{filename}
```

**Resposta:** Arquivo (imagem)

---

## 💻 EXEMPLOS DE USO NO FRONTEND

### JavaScript/Fetch

```javascript
const API_URL = 'https://projeto-jornadadados-pet-api-adoptt.zjnxkg.easypanel.host';

// Buscar todos os cães disponíveis
const getDogs = async () => {
  const response = await fetch(`${API_URL}/pets?species=dog&status=available`);
  const data = await response.json();
  return data.pets;
};

// Buscar pets por cidade
const getPetsByCity = async (city) => {
  const response = await fetch(`${API_URL}/pets?city=${city}`);
  const data = await response.json();
  return data.pets;
};

// Buscar por nome
const searchPets = async (query) => {
  const response = await fetch(`${API_URL}/pets/search?q=${query}`);
  const data = await response.json();
  return data.pets;
};

// Criar usuário
const createUser = async (userData) => {
  const response = await fetch(`${API_URL}/users`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(userData)
  });
  return await response.json();
};

// Adotar pet
const adoptPet = async (petId, userId) => {
  const response = await fetch(`${API_URL}/pets/${petId}/adopt`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ user_id: userId })
  });
  return await response.json();
};

// Upload de fotos
const uploadPhotos = async (petId, files) => {
  const formData = new FormData();
  files.forEach(file => {
    formData.append('files', file);
  });
  
  const response = await fetch(`${API_URL}/pets/${petId}/photos`, {
    method: 'POST',
    body: formData
  });
  return await response.json();
};

// Obter estatísticas
const getStats = async () => {
  const response = await fetch(`${API_URL}/pets/stats`);
  return await response.json();
};
```

### React Hooks

```javascript
import { useState, useEffect } from 'react';

const usePets = () => {
  const [pets, setPets] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchPets = async (filters = {}) => {
    setLoading(true);
    const params = new URLSearchParams(filters);
    const response = await fetch(`${API_URL}/pets?${params}`);
    const data = await response.json();
    setPets(data.pets);
    setLoading(false);
  };

  useEffect(() => {
    fetchPets();
  }, []);

  return { pets, loading, fetchPets };
};

const useUsers = () => {
  const [users, setUsers] = useState([]);

  const createUser = async (userData) => {
    const response = await fetch(`${API_URL}/users`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    });
    const newUser = await response.json();
    setUsers([...users, newUser]);
    return newUser;
  };

  return { users, createUser };
};
```

---

## 🐕🐱 DADOS DISPONÍVEIS

### Cães (15 pets únicos):
- Luna, Max, Bella, Thor, Lola, Zeus, Maya, Apollo, Nala, Rocky, Sofia, Bruno, Rex, Karen, Charlie

### Gatos (15 pets únicos):
- Mimi, Simba, Carminha, Felix, BellaCat, Garfield, NalaCat, Pink, MayaCat, Whiskers, Laly, Shadow, Brina, Tiger, Mia

### Cidades disponíveis:
- São Paulo, Rio de Janeiro, Belo Horizonte, Salvador, Brasília, Fortaleza, Manaus, Curitiba, Recife, Porto Alegre

### Estrutura dos dados:
- **Espécie**: `dog` ou `cat`
- **Gênero**: `male` ou `female`
- **Status**: `available` ou `adopted`
- **Fotos**: URLs do Unsplash (únicas para cada pet)
- **Idades**: Variadas (8-42 meses)

---

## 🔧 CORS
A API está configurada para aceitar requisições de qualquer origem (`*`), então não há problemas de CORS no frontend.

---

## 📝 Notas Importantes

1. **Paginação**: Use `page` e `limit` para controlar a quantidade de dados
2. **Filtros**: Combine múltiplos filtros na mesma requisição
3. **Upload**: Use FormData para upload de imagens
4. **Validação**: A API valida todos os dados automaticamente
5. **Erros**: Retorna códigos HTTP apropriados (400, 404, 500, etc.)

---

**API pronta para uso! 🚀**
