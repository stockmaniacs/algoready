"""Broker integration routes for AlgoReady."""

from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

router = APIRouter()


class BrokerType(str, Enum):
    zerodha = "zerodha"
    upstox = "upstox"
    fyers = "fyers"


class BrokerConnectionResponse(BaseModel):
    """Response model for broker connection status."""
    id: str
    broker: BrokerType
    account_name: str
    account_number: str
    is_connected: bool
    last_synced: Optional[str] = None
    instruments_count: int = 0


@router.get("/", response_model=List[BrokerConnectionResponse])
async def list_brokers():
    """List all connected brokers for the user."""
    # TODO: Implement with database
    return []


@router.post("/{broker}/connect")
async def connect_broker(broker: BrokerType, redirect_uri: str = Query(None)):
    """Initiate broker connection flow."""
    # TODO: Implement OAuth flow
    return {
        "message": f"Connect flow initiated for {broker.value}",
        "redirect_url": f"https://broker.example.com/oauth?client_id=algoready&redirect_uri={redirect_uri}"
    }


@router.get("/{broker}/callback")
async def broker_callback(broker: BrokerType, code: str, state: str):
    """Handle OAuth callback from broker."""
    # TODO: Implement token exchange
    return {
        "message": f"Callback received for {broker.value}",
        "code": code
    }


@router.delete("/{broker_id}")
async def disconnect_broker(broker_id: str):
    """Disconnect a broker account."""
    return {"message": "Broker disconnected successfully"}