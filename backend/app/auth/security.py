"""Security utilities for AlgoReady."""

from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
import secrets
import hashlib
import os

# Secret key for JWT (should be from environment in production)
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def authenticate_user(email: str, password: str) -> Optional[dict]:
    """Authenticate a user."""
    # TODO: Implement with database
    # This is a placeholder - replace with actual user lookup
    mock_users = {
        "demo@algoready.dev": {
            "id": "user_1",
            "email": "demo@algoready.dev",
            "hashed_password": get_password_hash("demo123"),
            "full_name": "Demo User",
            "is_active": True
        }
    }
    
    user = mock_users.get(email)
    if not user:
        return None
    
    if not verify_password(password, user["hashed_password"]):
        return None
    
    return user


def generate_oauth_state() -> str:
    """Generate a secure OAuth state parameter."""
    return secrets.token_urlsafe(32)


def hash_token(token: str) -> str:
    """Hash a token for secure storage."""
    return hashlib.sha256(token.encode()).hexdigest()