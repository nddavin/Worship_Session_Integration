from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from jose import jwt
from jose.exceptions import JWTError
from typing import Any, Dict
from datetime import datetime, timedelta, timezone
import os

# Assuming these functions are defined in another module
from auth_utils import create_access_token, create_refresh_token, verify_password

# Assuming get_db is defined in a separate module, for example, database.py
from database import get_db

# Assuming User and Audio models are defined in models.py
from models import User, Audio, Playlist

# Configure the router
router = APIRouter()

# Define the login endpoint
@router.post("/login", response_model=Dict[str, Any])
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    # Create access and refresh tokens
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
        "refresh_token_expires_in": os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", "30"),
        "access_token_expires_in": os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15")
    }

# Define the refresh endpoint
@router.post("/refresh", response_model=Dict[str, Any])
def refresh(
    refresh_token: str = Form(...),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    try:
        # Decode the refresh token
        refresh_token_data = jwt.decode(
            refresh_token,
            os.getenv("JWT_SECRET_KEY", ""),
            algorithms=[os.getenv("JWT_ALGORITHM", "HS256")]
        )
        username = refresh_token_data.get("sub")
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        # Create a new access token
        access_token = create_access_token(data={"sub": user.username})

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "access_token_expires_in": os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15")
        }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
