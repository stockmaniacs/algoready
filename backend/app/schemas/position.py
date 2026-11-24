"""Position schemas."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class PositionDirection(str):
    """Position direction."""
    LONG = "LONG"
    SHORT = "SHORT"


class PositionBase(BaseModel):
    """Base position schema."""
    instrument: str
    exchange: str
    direction: str = Field(..., pattern="^(LONG|SHORT)$")
    quantity: float = Field(..., gt=0)
    avg_entry_price: float = Field(..., gt=0)
    current_price: Optional[float] = None
    unrealized_pnl: Optional[float] = None
    realized_pnl: float = 0.0
    product_type: Optional[str] = None


class PositionCreate(PositionBase):
    """Schema for creating a position."""
    broker_connection_id: str


class PositionUpdate(BaseModel):
    """Schema for updating a position."""
    quantity: Optional[float] = None
    avg_entry_price: Optional[float] = None
    current_price: Optional[float] = None
    unrealized_pnl: Optional[float] = None
    realized_pnl: Optional[float] = None


class PositionResponse(PositionBase):
    """Schema for position response."""
    id: str
    user_id: str
    broker_connection_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class PositionList(BaseModel):
    """Paginated position list."""
    positions: List[PositionResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class PositionSummary(BaseModel):
    """Position summary with aggregated metrics."""
    total_positions: int
    long_positions: int
    short_positions: int
    total_unrealized_pnl: float
    total_realized_pnl: float
    total_invested: float
    day_pnl: float


class ClosePositionRequest(BaseModel):
    """Request to close a position."""
    position_id: str
    broker_connection_id: str
    quantity: Optional[float] = None  # Partial close if specified
    price: Optional[float] = None  # Limit price if specified
    order_type: str = Field(default="MARKET", pattern="^(MARKET|LIMIT)$")


class PositionPnLResponse(BaseModel):
    """Position P&L breakdown."""
    position_id: str
    instrument: str
    direction: str
    quantity: float
    avg_entry_price: float
    current_price: float
    unrealized_pnl: float
    realized_pnl: float
    pnl_percent: float
    day_change: float
    day_change_percent: float