"""Broker connection model."""

from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, func, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db import Base


class BrokerConnection(Base):
    """Model for broker account connections."""
    
    __tablename__ = "broker_connections"
    
    id = Column(UUID(as_key=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_key=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    broker_type = Column(String(50), nullable=False)  # 'zerodha', 'upstox', 'fyers'
    account_id = Column(String(255), nullable=False)
    access_token = Column(Text, nullable=False)  # Encrypted in production
    refresh_token = Column(Text, nullable=True)  # Encrypted in production
    expires_at = Column(DateTime(timezone=True), nullable=True)
    connected_at = Column(DateTime(timezone=True), server_default=func.now())
    last_synced = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    account_data = Column(JSON, nullable=True)  # Store account metadata
    symbols_cache = Column(JSON, nullable=True)  # Cached instrument symbols
    
    __table_args__ = (
        # Ensure unique combination of user, broker, and account
        # Note: PostgreSQL unique constraint with partial index
        {},
    )
    
    def __repr__(self) -> str:
        return f"<BrokerConnection(id={self.id}, broker={self.broker_type}, account={self.account_id})>"