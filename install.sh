#!/bin/bash

echo "🚀 Instalando Pet Adoption API..."

# Atualizar sistema
sudo apt update

# Instalar Python e dependências
sudo apt install -y python3 python3-pip python3-venv

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Inicializar banco
python database.py

# Iniciar API
echo "✅ API instalada! Iniciando..."
uvicorn main:app --host 0.0.0.0 --port 8000
