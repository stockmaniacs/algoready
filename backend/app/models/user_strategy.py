"""User strategy model - tracks strategies applied by users."""

from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, func, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db import Base


class UserStrategy(Base):
    """Model for user-applied strategies."""
    
    __tablename__ = "user_strategies"
    
    id = Column(UUID(as_key=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_key=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    strategy_id = Column(UUID(as_key=True), ForeignKey("strategies.id", ondelete="CASCADE"), nullable=False)
    broker_connection_id = Column(UUID(as_key=True), ForeignKey("broker_connections.id", ondelete="SET NULL"), nullable=True)
    applied_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    configuration = Column(JSON, nullable=True)  # User-specific parameter overrides
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    __table_args__ = (
        {},
    )
    
    def __repr__(self) -> str:
        return f"<UserStrategy(id={self.id}, user_id={self.user_id}, strategy_id={self.strategy_id})>"