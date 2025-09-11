#!/bin/bash

echo "🚀 Deploy Pet Adoption API para VPS"
echo "=================================="

# Atualizar sistema
echo "📦 Atualizando sistema..."
sudo apt update && sudo apt upgrade -y

# Instalar Python e dependências
echo "🐍 Instalando Python..."
sudo apt install python3 python3-pip python3-venv nginx -y

# Criar diretório da aplicação
echo "📁 Criando diretório da aplicação..."
sudo mkdir -p /var/www/pet-api
sudo chown $USER:$USER /var/www/pet-api

# Clonar repositório
echo "📥 Clonando repositório..."
cd /var/www/pet-api
git clone https://github.com/lanroo/pet-api-adopt.git .

# Criar ambiente virtual
echo "🔧 Criando ambiente virtual..."
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
echo "📚 Instalando dependências..."
pip install -r requirements.txt

# Inicializar banco de dados
echo "🗄️ Inicializando banco de dados..."
python database.py

# Criar arquivo de serviço systemd
echo "⚙️ Criando serviço systemd..."
sudo tee /etc/systemd/system/pet-api.service > /dev/null <<EOF
[Unit]
Description=Pet Adoption API
After=network.target

[Service]
Type=exec
User=$USER
WorkingDirectory=/var/www/pet-api
Environment=PATH=/var/www/pet-api/venv/bin
ExecStart=/var/www/pet-api/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Configurar Nginx
echo "🌐 Configurando Nginx..."
sudo tee /etc/nginx/sites-available/pet-api > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Ativar site
sudo ln -sf /etc/nginx/sites-available/pet-api /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Reiniciar serviços
echo "🔄 Reiniciando serviços..."
sudo systemctl daemon-reload
sudo systemctl enable pet-api
sudo systemctl start pet-api
sudo systemctl restart nginx

echo "✅ Deploy concluído!"
echo "🌐 API disponível em: http://SEU_IP"
echo "📚 Swagger em: http://SEU_IP/docs"
echo "🔍 Health check: http://SEU_IP/health"
echo ""
echo "📋 Comandos úteis:"
echo "sudo systemctl status pet-api    # Status do serviço"
echo "sudo systemctl restart pet-api   # Reiniciar API"
echo "sudo journalctl -u pet-api -f    # Ver logs"
