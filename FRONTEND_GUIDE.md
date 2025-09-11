# 🐾 Pet Adoption API - Guia para Frontend

## 📋 Informações da API

### 🌐 URL Base da API:
```javascript
const API_BASE_URL = 'https://pet-adoption-cw31c6uqt-lanroos-projects.vercel.app';
```

### 📚 Documentação Swagger:
```
https://pet-adoption-cw31c6uqt-lanroos-projects.vercel.app/docs
```

### 🔍 Health Check:
```
https://pet-adoption-cw31c6uqt-lanroos-projects.vercel.app/health
```

---

## 🔗 Endpoints Disponíveis

### 🐾 Pets

#### Listar todos os pets (com filtros)
```http
GET /pets?species=dog&city=São Paulo&status=available&page=1&limit=10
```

**Parâmetros de query:**
- `species`: dog, cat
- `city`: qualquer cidade
- `status`: available, adopted
- `page`: número da página (começa em 1)
- `limit`: itens por página (máximo 100)

**Resposta:**
```json
{
  "pets": [...],
  "total": 30,
  "page": 1,
  "limit": 10
}
```

#### Buscar pet específico
```http
GET /pets/{id}
```

#### Criar novo pet
```http
POST /pets
Content-Type: application/json

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

#### Atualizar pet
```http
PUT /pets/{id}
Content-Type: application/json

{
  "name": "Luna Atualizada",
  "description": "Nova descrição"
}
```

#### Deletar pet
```http
DELETE /pets/{id}
```

#### Buscar pets
```http
GET /pets/search?q=Luna
```

#### Estatísticas
```http
GET /pets/stats
```

**Resposta:**
```json
{
  "total_pets": 30,
  "available_pets": 30,
  "adopted_pets": 0
}
```

---

### 👤 Usuários

#### Listar usuários
```http
GET /users
```

#### Criar usuário
```http
POST /users
Content-Type: application/json

{
  "full_name": "João Silva",
  "email": "joao@email.com",
  "phone": "11999999999",
  "city": "São Paulo"
}
```

#### Buscar usuário
```http
GET /users/{id}
```

---

### 🏠 Adoção

#### Adotar pet
```http
POST /pets/{id}/adopt
Content-Type: application/json

{
  "user_id": 1
}
```

---

## 💻 Exemplos de Uso no Frontend

### React/JavaScript (Fetch)

```javascript
const API_BASE_URL = 'https://pet-adoption-cw31c6uqt-lanroos-projects.vercel.app';

// Listar pets
const fetchPets = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/pets`);
    const data = await response.json();
    return data.pets;
  } catch (error) {
    console.error('Erro ao buscar pets:', error);
  }
};

// Listar pets com filtros
const fetchPetsWithFilters = async (species, city, status) => {
  const params = new URLSearchParams();
  if (species) params.append('species', species);
  if (city) params.append('city', city);
  if (status) params.append('status', status);
  
  const response = await fetch(`${API_BASE_URL}/pets?${params}`);
  return response.json();
};

// Criar usuário
const createUser = async (userData) => {
  const response = await fetch(`${API_BASE_URL}/users`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData)
  });
  return response.json();
};

// Adotar pet
const adoptPet = async (petId, userId) => {
  const response = await fetch(`${API_BASE_URL}/pets/${petId}/adopt`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: userId })
  });
  return response.json();
};

// Buscar pets
const searchPets = async (query) => {
  const response = await fetch(`${API_BASE_URL}/pets/search?q=${encodeURIComponent(query)}`);
  return response.json();
};

// Obter estatísticas
const getStats = async () => {
  const response = await fetch(`${API_BASE_URL}/pets/stats`);
  return response.json();
};
```

### Axios

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://pet-adoption-cw31c6uqt-lanroos-projects.vercel.app'
});

// Listar pets
const pets = await api.get('/pets');

// Listar pets com filtros
const petsFiltered = await api.get('/pets', {
  params: { species: 'dog', city: 'São Paulo' }
});

// Criar usuário
const user = await api.post('/users', {
  full_name: 'João Silva',
  email: 'joao@email.com',
  phone: '11999999999',
  city: 'São Paulo'
});

// Adotar pet
const adoption = await api.post(`/pets/${petId}/adopt`, { 
  user_id: userId 
});

// Buscar pets
const searchResults = await api.get('/pets/search', {
  params: { q: 'Luna' }
});

// Estatísticas
const stats = await api.get('/pets/stats');
```

### React Hook Personalizado

```javascript
import { useState, useEffect } from 'react';

const usePets = () => {
  const [pets, setPets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchPets = async (filters = {}) => {
    try {
      setLoading(true);
      const params = new URLSearchParams(filters);
      const response = await fetch(`${API_BASE_URL}/pets?${params}`);
      const data = await response.json();
      setPets(data.pets);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPets();
  }, []);

  return { pets, loading, error, fetchPets };
};

// Uso no componente
const PetList = () => {
  const { pets, loading, error, fetchPets } = usePets();

  if (loading) return <div>Carregando...</div>;
  if (error) return <div>Erro: {error.message}</div>;

  return (
    <div>
      {pets.map(pet => (
        <div key={pet.id}>
          <h3>{pet.name}</h3>
          <p>{pet.breed} - {pet.species}</p>
          <p>{pet.city}</p>
        </div>
      ))}
    </div>
  );
};
```

---

## 📊 Dados Disponíveis na API

### 🐕 Cachorros: 15
- **Gêneros**: 8 fêmeas, 7 machos
- **Raças**: Golden Retriever, Pastor Alemão, Labrador, Bulldog, Poodle, Beagle, Rottweiler, Husky, Dachshund, Boxer, Chihuahua, Shih Tzu, Border Collie, Doberman, Maltês

### 🐱 Gatos: 15
- **Gêneros**: 7 machos, 8 fêmeas
- **Raças**: Persa, Siamês, Maine Coon, Ragdoll, British Shorthair, Abissínio, Birmanês, Sphynx, Scottish Fold, Angorá, Bombay, Manx, Oriental, Siberiano, Devon Rex

### 🏙️ Cidades: 10
São Paulo, Rio de Janeiro, Belo Horizonte, Salvador, Brasília, Fortaleza, Manaus, Curitiba, Recife, Porto Alegre

### 📈 Estatísticas
- **Total**: 30 pets
- **Disponíveis**: 30 pets
- **Adotados**: 0 pets

---

## 🔧 Configurações

### CORS
✅ **CORS habilitado** para qualquer origem - não precisa configurar nada!

### Headers
```javascript
// Headers necessários para POST/PUT
{
  'Content-Type': 'application/json'
}
```

### Tratamento de Erros
```javascript
const handleApiError = (error) => {
  if (error.response) {
    // Erro da API
    console.error('Erro da API:', error.response.data);
  } else if (error.request) {
    // Erro de rede
    console.error('Erro de rede:', error.request);
  } else {
    // Outros erros
    console.error('Erro:', error.message);
  }
};
```

---

## 🚀 Links Úteis

- **API**: https://pet-adoption-cw31c6uqt-lanroos-projects.vercel.app
- **Swagger**: https://pet-adoption-cw31c6uqt-lanroos-projects.vercel.app/docs
- **Health Check**: https://pet-adoption-cw31c6uqt-lanroos-projects.vercel.app/health
- **GitHub**: https://github.com/lanroo/pet-api-adopt.git

---

## 📝 Notas Importantes

1. **Todos os endpoints retornam JSON**
2. **CORS está habilitado para qualquer origem**
3. **A API está em produção e estável**
4. **30 pets de exemplo já estão cadastrados**
5. **Swagger disponível para testar endpoints**
6. **Paginação disponível para listagem de pets**
7. **Filtros disponíveis por espécie, cidade e status**

---

**🎉 Agora é só usar no seu frontend!**
