#!/bin/bash

echo "🧪 Testando Pet Adoption API..."
echo ""

# Health check
echo "1. Health Check:"
curl -s http://localhost:8000/health | jq .
echo ""

# Listar pets
echo "2. Listar pets:"
curl -s http://localhost:8000/pets | jq .
echo ""

# Estatísticas
echo "3. Estatísticas:"
curl -s http://localhost:8000/pets/stats | jq .
echo ""

# Buscar pets
echo "4. Buscar pets (termo: 'Luna'):"
curl -s "http://localhost:8000/pets/search?q=Luna" | jq .
echo ""

# Listar usuários
echo "5. Listar usuários:"
curl -s http://localhost:8000/users | jq .
echo ""

# Criar novo usuário
echo "6. Criar novo usuário:"
curl -s -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d '{"full_name": "Teste User", "email": "teste@example.com", "phone": "11999999999", "city": "São Paulo"}' | jq .
echo ""

# Criar novo pet
echo "7. Criar novo pet:"
curl -s -X POST "http://localhost:8000/pets" \
  -H "Content-Type: application/json" \
  -d '{"name": "Rex", "species": "dog", "breed": "Labrador", "age": 12, "gender": "male", "city": "São Paulo", "description": "Cachorro muito brincalhão"}' | jq .
echo ""

echo "✅ Testes concluídos!"
echo "📚 Acesse http://localhost:8000/docs para ver a documentação completa"
