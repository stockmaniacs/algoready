"""User model."""

from sqlalchemy import Column, String, DateTime, Boolean, func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db import Base


class User(Base):
    """User model for authentication and profile."""
    
    __tablename__ = "users"
    
    id = Column(UUID(as_key=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    email_verified = Column(Boolean, default=False)
    avatar_url = Column(String(500), nullable=True)
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"