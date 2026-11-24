"""Authentication routes for AlgoReady."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing import Optional

router = APIRouter()


# Models
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: Optional[str] = None


# Mock user storage (replace with database in production)
users_db = {}


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    """Register a new user."""
    if user.email in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # In production: hash password, save to database
    user_id = f"user_{len(users_db) + 1}"
    users_db[user.email] = {
        "id": user_id,
        "email": user.email,
        "full_name": user.full_name,
    }
    
    return UserResponse(id=user_id, email=user.email, full_name=user.full_name)


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login with email and password."""
    user = users_db.get(form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # In production: verify password, generate JWT
    return Token(access_token=f"mock_token_{user['id']}")


@router.get("/me", response_model=UserResponse)
async def get_current_user(token: str):
    """Get current user information."""
    # In production: decode JWT, get user from database
    return UserResponse(id="user_1", email="demo@algoready.dev", full_name="Demo User")