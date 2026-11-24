"""Strategy model."""

from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text, ForeignKey, func, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db import Base


class Strategy(Base):
    """Model for trading strategies."""
    
    __tablename__ = "strategies"
    
    id = Column(UUID(as_key=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=False)  # 'scalping', 'momentum', etc.
    market = Column(String(50), nullable=False)  # 'india_stocks', 'crypto', 'us_stocks'
    instrument_filter = Column(JSON, nullable=True)  # Pattern for applicable instruments
    timeframe = Column(String(20), nullable=False)
    parameters = Column(JSON, nullable=True)  # Strategy parameters
    entry_rules = Column(JSON, nullable=True)
    exit_rules = Column(JSON, nullable=True)
    target_percent = Column(Integer, nullable=False)
    stop_loss_percent = Column(Integer, nullable=False)
    risk_per_trade = Column(Integer, nullable=False)
    backtest_metrics = Column(JSON, nullable=True)
    created_by = Column(String(255), nullable=True)
    is_public = Column(Boolean, default=True)
    subscription_required = Column(Boolean, default=False)
    version = Column(String(20), default="1.0.0")
    slug = Column(String(255), unique=True, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self) -> str:
        return f"<Strategy(id={self.id}, name={self.name})>"