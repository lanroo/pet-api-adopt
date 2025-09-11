# 🚀 Deploy na VPS - Pet Adoption API

## 📋 Pré-requisitos

- VPS com Ubuntu/Debian
- Acesso SSH
- Python 3.8+
- Git

## 🔧 Deploy Automático

### 1. Conectar na VPS
```bash
ssh usuario@seu-ip
```

### 2. Executar script de deploy
```bash
# Baixar e executar o script
curl -o deploy_vps.sh https://raw.githubusercontent.com/lanroo/pet-api-adopt/main/deploy_vps.sh
chmod +x deploy_vps.sh
./deploy_vps.sh
```

## 🔧 Deploy Manual

### 1. Atualizar sistema
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv nginx git -y
```

### 2. Criar diretório da aplicação
```bash
sudo mkdir -p /var/www/pet-api
sudo chown $USER:$USER /var/www/pet-api
cd /var/www/pet-api
```

### 3. Clonar repositório
```bash
git clone https://github.com/lanroo/pet-api-adopt.git .
```

### 4. Configurar ambiente Python
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-vps.txt
```

### 5. Inicializar banco de dados
```bash
python database.py
```

### 6. Criar serviço systemd
```bash
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
```

### 7. Configurar Nginx
```bash
sudo cp nginx.conf /etc/nginx/sites-available/pet-api
sudo ln -sf /etc/nginx/sites-available/pet-api /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
```

### 8. Iniciar serviços
```bash
sudo systemctl daemon-reload
sudo systemctl enable pet-api
sudo systemctl start pet-api
sudo systemctl restart nginx
```

## 🌐 Acessos

- **API**: http://SEU_IP
- **Swagger**: http://SEU_IP/docs
- **Health Check**: http://SEU_IP/health

## 📋 Comandos Úteis

```bash
# Status do serviço
sudo systemctl status pet-api

# Reiniciar API
sudo systemctl restart pet-api

# Ver logs
sudo journalctl -u pet-api -f

# Parar API
sudo systemctl stop pet-api

# Iniciar API
sudo systemctl start pet-api
```

## 🔄 Atualizar API

```bash
cd /var/www/pet-api
git pull origin main
sudo systemctl restart pet-api
```

## 🛠️ Troubleshooting

### API não inicia
```bash
sudo journalctl -u pet-api -f
```

### Nginx não funciona
```bash
sudo nginx -t
sudo systemctl status nginx
```

### Porta 8000 ocupada
```bash
sudo lsof -i :8000
sudo kill -9 PID
```

## 🔒 Configurar HTTPS (Opcional)

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obter certificado
sudo certbot --nginx -d seu-dominio.com

# Renovação automática
sudo crontab -e
# Adicionar: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 📊 Monitoramento

```bash
# Ver uso de recursos
htop

# Ver logs em tempo real
sudo journalctl -u pet-api -f

# Verificar conectividade
curl http://localhost:8000/health
```

---

**🎉 Sua API estará rodando perfeitamente na VPS!**
