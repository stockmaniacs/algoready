"""Position management routes for AlgoReady."""

from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

router = APIRouter()


class PositionDirection(str, Enum):
    LONG = "LONG"
    SHORT = "SHORT"


class PositionResponse(BaseModel):
    """Position response model."""
    id: str
    broker: str
    account_number: str
    instrument: str
    exchange: str
    direction: PositionDirection
    quantity: float
    avg_entry_price: float
    current_price: float
    unrealized_pnl: float
    realized_pnl: float = 0.0
    product_type: str
    created_at: datetime
    updated_at: datetime


class PositionSummary(BaseModel):
    """Summary of positions for a user."""
    total_positions: int
    total_unrealized_pnl: float
    total_realized_pnl: float
    total_invested: float
    total_value: float


@router.get("/", response_model=List[PositionResponse])
async def list_positions(
    broker: Optional[str] = Query(None),
    exchange: Optional[str] = Query(None)
):
    """List all positions for the user."""
    # TODO: Implement with database
    return []


@router.get("/summary", response_model=PositionSummary)
async def get_position_summary():
    """Get position summary."""
    return PositionSummary(
        total_positions=0,
        total_unrealized_pnl=0.0,
        total_realized_pnl=0.0,
        total_invested=0.0,
        total_value=0.0
    )


@router.get("/{instrument}", response_model=PositionResponse)
async def get_position(instrument: str, broker: Optional[str] = Query(None)):
    """Get position for specific instrument."""
    raise HTTPException(status_code=404, detail="Position not found")