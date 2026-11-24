"""Order management routes for AlgoReady."""

from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

router = APIRouter()


class TransactionType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    SL_MARKET = "SL-MARKET"
    SL_LIMIT = "SL-LIMIT"


class ProductType(str, Enum):
    CNC = "CNC"  # Cash and Carry
    MIS = "MIS"  # Margin Intraday Square Off
    NRML = "NRML"  # Normal
    CO = "CO"  # Cover Order
    BO = "BO"  # Bracket Order
    IC = "IC"  # Intraday Square Off


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    OPEN = "OPEN"
    CANCELLED = "CANCELLED"
    COMPLETE = "COMPLETE"
    REJECTED = "REJECTED"
    TRIGGERED = "TRIGGERED"


class OrderResponse(BaseModel):
    """Order response model."""
    id: str
    broker_order_id: str
    instrument: str
    exchange: str
    transaction_type: TransactionType
    order_type: OrderType
    product: ProductType
    quantity: float
    price: Optional[float] = None
    trigger_price: Optional[float] = None
    status: OrderStatus
    filled_quantity: float = 0.0
    average_price: Optional[float] = None
    placed_at: datetime
    updated_at: datetime


class PlaceOrderRequest(BaseModel):
    """Request model for placing an order."""
    instrument: str
    exchange: str
    transaction_type: TransactionType
    order_type: OrderType = OrderType.MARKET
    product: ProductType = ProductType.MIS
    quantity: float = Field(..., gt=0)
    price: Optional[float] = Field(None, gt=0)
    trigger_price: Optional[float] = Field(None, gt=0)
    broker_id: Optional[str] = None
    signal_id: Optional[str] = None

    @field_validator('price')
    @classmethod
    def validate_price(cls, v, info):
        if info.data.get('order_type') in [OrderType.LIMIT, OrderType.SL_LIMIT] and v is None:
            raise ValueError('Price is required for LIMIT and SL-LIMIT orders')
        return v


class OrderPreview(BaseModel):
    """Order preview response."""
    broker: str
    account: str
    instrument: str
    exchange: str
    transaction_type: TransactionType
    quantity: float
    order_type: OrderType
    product: ProductType
    price: Optional[float] = None
    trigger_price: Optional[float] = None
    estimated_charges: float
    available_margin: float
    strategy_name: Optional[str] = None


@router.get("/", response_model=List[OrderResponse])
async def list_orders(
    status: Optional[OrderStatus] = Query(None),
    broker: Optional[str] = Query(None),
    limit: int = Query(100, le=100)
):
    """List orders for the user."""
    # TODO: Implement with database
    return []


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def place_order(request: PlaceOrderRequest):
    """Place a new order."""
    # TODO: Implement with broker integration
    return OrderResponse(
        id=f"order_{datetime.now().timestamp()}",
        broker_order_id=f"broker_{datetime.now().timestamp()}",
        instrument=request.instrument,
        exchange=request.exchange,
        transaction_type=request.transaction_type,
        order_type=request.order_type,
        product=request.product,
        quantity=request.quantity,
        price=request.price,
        trigger_price=request.trigger_price,
        status=OrderStatus.PENDING,
        placed_at=datetime.now(),
        updated_at=datetime.now()
    )


@router.post("/preview", response_model=OrderPreview)
async def preview_order(request: PlaceOrderRequest):
    """Preview an order before placing."""
    return OrderPreview(
        broker="demo",
        account="demo_account",
        instrument=request.instrument,
        exchange=request.exchange,
        transaction_type=request.transaction_type,
        quantity=request.quantity,
        order_type=request.order_type,
        product=request.product,
        price=request.price,
        trigger_price=request.trigger_price,
        estimated_charges=0.0,
        available_margin=100000.0,
        strategy_name=None
    )


@router.put("/{order_id}", response_model=OrderResponse)
async def modify_order(order_id: str, request: dict):
    """Modify an existing order."""
    # TODO: Implement with broker integration
    raise HTTPException(status_code=404, detail="Order not found")


@router.delete("/{order_id}", response_model=dict)
async def cancel_order(order_id: str):
    """Cancel an order."""
    # TODO: Implement with broker integration
    return {"message": "Order cancelled successfully"}