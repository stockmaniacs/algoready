"""Order model - trading orders."""

from sqlalchemy import Column, String, DateTime, Boolean, Integer, Float, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db import Base


class Order(Base):
    """Model for trading orders."""
    
    __tablename__ = "orders"
    
    id = Column(UUID(as_key=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_key=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    broker_connection_id = Column(UUID(as_key=True), ForeignKey("broker_connections.id", ondelete="SET NULL"), nullable=True)
    signal_id = Column(UUID(as_key=True), ForeignKey("signals.id", ondelete="SET NULL"), nullable=True)
    
    exchange = Column(String(50), nullable=False)
    instrument = Column(String(255), nullable=False)
    transaction_type = Column(String(10), nullable=False)
    order_type = Column(String(20), nullable=False)
    product = Column(String(10), nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=True)
    trigger_price = Column(Float, nullable=True)
    
    status = Column(String(50), default="PENDING")
    broker_order_id = Column(String(255), nullable=True)
    filled_quantity = Column(Float, default=0.0)
    average_price = Column(Float, nullable=True)
    
    placed_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self) -> str:
        return f"<Order(id={self.id}, instrument={self.instrument}, status={self.status})>"