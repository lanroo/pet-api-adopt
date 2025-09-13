from datetime import datetime, timedelta
from typing import Optional
import os

try:
    from passlib.context import CryptContext
    from jose import jwt, JWTError
    AUTH_DEPS_INSTALLED = True
except ImportError:
    AUTH_DEPS_INSTALLED = False
    CryptContext = None
    jwt = None
    JWTError = None

# Configurações JWT
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60  # 24 horas

# Contexto para hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar senha"""
    if not AUTH_DEPS_INSTALLED:
        return plain_password == hashed_password  # Fallback para teste sem deps
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Gerar hash da senha"""
    if not AUTH_DEPS_INSTALLED:
        return password  # Fallback para teste sem deps
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Criar token JWT"""
    if not AUTH_DEPS_INSTALLED:
        return "mock-token"  # Fallback para teste sem deps
    
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """Verificar token JWT"""
    if not AUTH_DEPS_INSTALLED:
        return {"sub": "1", "email": "test@example.com"}  # Fallback para teste
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def check_dependencies():
    """Verificar se as dependências estão instaladas"""
    return AUTH_DEPS_INSTALLED
