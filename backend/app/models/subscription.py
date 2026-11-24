"""Subscription model - user subscription plans."""

from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db import Base


class Subscription(Base):
    """Model for user subscriptions."""
    
    __tablename__ = "subscriptions"
    
    id = Column(UUID(as_key=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_key=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    plan_type = Column(String(50), nullable=False)  # 'free', 'pro', 'premium'
    payment_id = Column(String(255), nullable=True)
    status = Column(String(50), default="active")  # 'active', 'expired', 'cancelled'
    
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self) -> str:
        return f"<Subscription(id={self.id}, plan={self.plan_type}, status={self.status})>"