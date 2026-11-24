"""Broker connection schemas."""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class BrokerType(str):
    """Supported broker types."""
    ZERODHA = "zerodha"
    UPSTOX = "upstox"
    FYERS = "fyers"


class BrokerConnectionBase(BaseModel):
    """Base broker connection schema."""
    broker_type: str = Field(..., pattern="^(zerodha|upstox|fyers)$")
    account_id: str
    # Note: tokens are handled separately for security


class BrokerConnectionCreate(BrokerConnectionBase):
    """Schema for creating a broker connection."""
    access_token: str
    refresh_token: Optional[str] = None
    expires_at: Optional[datetime] = None


class BrokerConnectionUpdate(BaseModel):
    """Schema for updating a broker connection."""
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_at: Optional[datetime] = None
    is_active: Optional[bool] = None
    account_data: Optional[Dict[str, Any]] = None
    symbols_cache: Optional[Dict[str, Any]] = None
    last_synced: Optional[datetime] = None


class BrokerConnectionResponse(BrokerConnectionBase):
    """Schema for broker connection response."""
    id: str
    user_id: str
    connected_at: datetime
    expires_at: Optional[datetime] = None
    last_synced: Optional[datetime] = None
    is_active: bool
    account_data: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)


class BrokerConnectionList(BaseModel):
    """List of broker connections."""
    connections: list[BrokerConnectionResponse]
    total: int


class BrokerAuthRequest(BaseModel):
    """Request to initiate broker authentication."""
    broker_type: str = Field(..., pattern="^(zerodha|upstox|fyers)$")


class BrokerAuthResponse(BaseModel):
    """Broker authentication response with redirect URL."""
    auth_url: str
    state: str


class BrokerCallbackRequest(BaseModel):
    """Broker OAuth callback request."""
    broker_type: str
    code: str
    state: str


class BrokerAccountInfo(BaseModel):
    """Broker account information."""
    user_id: str
    user_name: str
    email: str
    broker_type: str
    account_type: str
    balance: Optional[float] = None
    margin: Optional[float] = None


class BrokerSyncRequest(BaseModel):
    """Request to sync broker data."""
    broker_connection_id: str
    sync_type: str = Field(default="full", pattern="^(full|positions|orders|holdings)$")


class BrokerSyncResponse(BaseModel):
    """Broker sync response."""
    success: bool
    message: str
    synced_at: datetime
    positions_count: int = 0
    orders_count: int = 0
    holdings_count: int = 0