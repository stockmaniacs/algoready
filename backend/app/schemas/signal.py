"""Signal schemas."""

from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, ConfigDict


class SignalDirection(str):
    """Signal direction."""
    LONG = "LONG"
    SHORT = "SHORT"


class SignalStatus(str):
    """Signal status."""
    PENDING = "pending"
    EXECUTED = "executed"
    INVALIDATED = "invalidated"
    EXPIRED = "expired"
    PARTIAL = "partial"


class SignalBase(BaseModel):
    """Base signal schema."""
    instrument: str
    exchange: str
    direction: str = Field(..., pattern="^(LONG|SHORT)$")
    entry_price: Optional[float] = None
    target_price: float
    stop_loss_price: float
    risk_reward_ratio: Optional[float] = None
    expires_at: Optional[datetime] = None


class SignalCreate(SignalBase):
    """Schema for creating a signal."""
    strategy_id: str
    broker_connection_id: Optional[str] = None


class SignalUpdate(BaseModel):
    """Schema for updating a signal."""
    entry_price: Optional[float] = None
    target_price: Optional[float] = None
    stop_loss_price: Optional[float] = None
    status: Optional[str] = None
    order_id: Optional[str] = None
    filled_quantity: Optional[float] = None


class SignalResponse(SignalBase):
    """Schema for signal response."""
    id: str
    user_id: str
    strategy_id: str
    broker_connection_id: Optional[str] = None
    status: str
    order_id: Optional[str] = None
    filled_quantity: float
    detected_at: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class SignalList(BaseModel):
    """Paginated signal list."""
    signals: List[SignalResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class SignalExecuteRequest(BaseModel):
    """Request to execute a signal."""
    signal_id: str
    broker_connection_id: str
    quantity: Optional[float] = None
    price: Optional[float] = None
    order_type: str = Field(default="MARKET", pattern="^(MARKET|LIMIT|SL|SLM)$")


class SignalBulkExecuteRequest(BaseModel):
    """Request to execute multiple signals."""
    signal_ids: List[str]
    broker_connection_id: str