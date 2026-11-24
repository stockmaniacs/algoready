"""User schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a user."""
    password: str = Field(..., min_length=8, max_length=128)


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    full_name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: Optional[bool] = None
    email_verified: Optional[bool] = None


class UserResponse(UserBase):
    """Schema for user response."""
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_active: bool
    email_verified: bool

    model_config = ConfigDict(from_attributes=True)


class UserWithSubscription(UserResponse):
    """User with subscription info."""
    subscription: Optional["SubscriptionResponse"] = None


# Import at bottom to avoid circular imports
from app.schemas.subscription import SubscriptionResponse  # noqa: E402