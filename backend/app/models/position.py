"""Position model - tracks open positions."""

from sqlalchemy import Column, String, DateTime, Boolean, Integer, Float, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db import Base


class Position(Base):
    """Model for tracking positions."""
    
    __tablename__ = "positions"
    
    id = Column(UUID(as_key=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_key=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    broker_connection_id = Column(UUID(as_key=True), ForeignKey("broker_connections.id", ondelete="SET NULL"), nullable=True)
    
    instrument = Column(String(255), nullable=False)
    exchange = Column(String(50), nullable=False)
    direction = Column(String(10), nullable=False)
    quantity = Column(Float, nullable=False)
    avg_entry_price = Column(Float, nullable=False)
    current_price = Column(Float, nullable=True)
    unrealized_pnl = Column(Float, nullable=True)
    realized_pnl = Column(Float, default=0.0)
    product_type = Column(String(50), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self) -> str:
        return f"<Position(id={self.id}, instrument={self.instrument}, quantity={self.quantity})>"