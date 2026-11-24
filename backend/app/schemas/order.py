"""Order schemas."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class OrderStatus(str):
    """Order status."""
    PENDING = "PENDING"
    OPEN = "OPEN"
    COMPLETE = "COMPLETE"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"
    PARTIAL = "PARTIAL"
    TRIGGER_PENDING = "TRIGGER_PENDING"


class OrderType(str):
    """Order type."""
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    SL = "SL"          # Stop Loss
    SLM = "SLM"        # Stop Loss Market


class TransactionType(str):
    """Transaction type."""
    BUY = "BUY"
    SELL = "SELL"


class ProductType(str):
    """Product type."""
    CNC = "CNC"        # Cash and Carry (Delivery)
    MIS = "MIS"        # Margin Intraday Square-off
    NRML = "NRML"      # Normal (Overnight)
    CO = "CO"          # Cover Order
    BO = "BO"          # Bracket Order


class OrderBase(BaseModel):
    """Base order schema."""
    exchange: str
    instrument: str
    transaction_type: str = Field(..., pattern="^(BUY|SELL)$")
    order_type: str = Field(..., pattern="^(MARKET|LIMIT|SL|SLM)$")
    product: str = Field(..., pattern="^(CNC|MIS|NRML|CO|BO)$")
    quantity: float = Field(..., gt=0)
    price: Optional[float] = None
    trigger_price: Optional[float] = None


class OrderCreate(OrderBase):
    """Schema for creating an order."""
    broker_connection_id: str
    signal_id: Optional[str] = None


class OrderUpdate(BaseModel):
    """Schema for updating an order."""
    status: Optional[str] = None
    broker_order_id: Optional[str] = None
    filled_quantity: Optional[float] = None
    average_price: Optional[float] = None


class OrderResponse(OrderBase):
    """Schema for order response."""
    id: str
    user_id: str
    broker_connection_id: Optional[str] = None
    signal_id: Optional[str] = None
    status: str
    broker_order_id: Optional[str] = None
    filled_quantity: float
    average_price: Optional[float] = None
    placed_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class OrderList(BaseModel):
    """Paginated order list."""
    orders: List[OrderResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class OrderPlaceRequest(BaseModel):
    """Request to place an order."""
    broker_connection_id: str
    exchange: str
    instrument: str
    transaction_type: str = Field(..., pattern="^(BUY|SELL)$")
    order_type: str = Field(default="MARKET", pattern="^(MARKET|LIMIT|SL|SLM)$")
    product: str = Field(default="MIS", pattern="^(CNC|MIS|NRML|CO|BO)$")
    quantity: float = Field(..., gt=0)
    price: Optional[float] = None
    trigger_price: Optional[float] = None
    signal_id: Optional[str] = None


class OrderModifyRequest(BaseModel):
    """Request to modify an order."""
    order_id: str
    broker_connection_id: str
    quantity: Optional[float] = None
    price: Optional[float] = None
    trigger_price: Optional[float] = None
    order_type: Optional[str] = None


class OrderCancelRequest(BaseModel):
    """Request to cancel an order."""
    order_id: str
    broker_connection_id: str


class OrderHistoryResponse(BaseModel):
    """Order history response."""
    orders: List[OrderResponse]
    total: int