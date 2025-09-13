from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from models import User
from auth import verify_token
from schemas import TokenData

def get_current_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get the current authenticated user
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        if not authorization or not authorization.startswith("Bearer "):
            raise credentials_exception
        
        token = authorization.split(" ")[1]
        payload = verify_token(token)
        
        if payload is None:
            raise credentials_exception

        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception

        user = db.query(User).filter(User.id == int(user_id)).first()
        if user is None:
            raise credentials_exception

        return user
    except Exception:
        raise credentials_exception

def get_current_user_optional(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Optional dependency to get the current authenticated user
    Returns None if not authenticated
    """
    try:
        if not authorization or not authorization.startswith("Bearer "):
            return None
        
        token = authorization.split(" ")[1]
        payload = verify_token(token)
        
        if payload is None:
            return None

        user_id: str = payload.get("sub")
        if user_id is None:
            return None

        user = db.query(User).filter(User.id == int(user_id)).first()
        return user
    except Exception:
        return None
