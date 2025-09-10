#!/bin/bash

echo "🐾 Iniciando Pet Adoption API..."

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências se necessário
echo "📚 Verificando dependências..."
pip install -q fastapi "uvicorn[standard]" sqlalchemy "pydantic[email]" python-multipart python-dotenv

# Inicializar banco de dados
echo "🗄️ Inicializando banco de dados..."
python database.py

# Iniciar servidor
echo "🚀 Iniciando servidor..."
echo ""
echo "✅ API rodando em: http://localhost:8000"
echo "📚 Documentação: http://localhost:8000/docs"
echo "🔍 Health check: http://localhost:8000/health"
echo ""
echo "Pressione Ctrl+C para parar o servidor"
echo ""

uvicorn main:app --reload --host 0.0.0.0 --port 8000
