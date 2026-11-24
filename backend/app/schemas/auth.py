"""Authentication schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class Token(BaseModel):
    """JWT token schema."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 3600  # 1 hour in seconds


class TokenData(BaseModel):
    """Token payload data."""
    sub: str
    email: EmailStr
    exp: datetime
    iat: datetime
    type: str = "access"


class LoginRequest(BaseModel):
    """Login request schema."""
    email: EmailStr
    password: str = Field(..., min_length=1)


class RegisterRequest(BaseModel):
    """Registration request schema."""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    full_name: Optional[str] = None
    phone: Optional[str] = None


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema."""
    refresh_token: str


class PasswordResetRequest(BaseModel):
    """Password reset request schema."""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation schema."""
    token: str
    new_password: str = Field(..., min_length=8, max_length=128)


class EmailVerificationRequest(BaseModel):
    """Email verification request schema."""
    email: EmailStr


class EmailVerificationConfirm(BaseModel):
    """Email verification confirmation schema."""
    token: str