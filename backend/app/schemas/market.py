"""Market data schemas."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class QuoteRequest(BaseModel):
    """Request for market quotes."""
    instruments: List[str] = Field(..., min_length=1, max_length=100)
    exchange: str = Field(default="NSE")


class QuoteData(BaseModel):
    """Quote data for a single instrument."""
    instrument: str
    exchange: str
    last_price: float
    change: float
    change_percent: float
    open: float
    high: float
    low: float
    close: float
    volume: int
    avg_price: Optional[float] = None
    oi: Optional[int] = None  # Open interest for derivatives
    timestamp: datetime
    bid_price: Optional[float] = None
    ask_price: Optional[float] = None
    bid_qty: Optional[int] = None
    ask_qty: Optional[int] = None
    depth: Optional[Dict[str, Any]] = None  # Market depth


class QuoteResponse(BaseModel):
    """Response with multiple quotes."""
    quotes: List[QuoteData]
    timestamp: datetime


class MarketDataResponse(BaseModel):
    """Generic market data response."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class InstrumentRequest(BaseModel):
    """Request to search instruments."""
    query: str = Field(..., min_length=1)
    exchange: Optional[str] = None
    segment: Optional[str] = None
    limit: int = Field(default=20, ge=1, le=100)


class InstrumentData(BaseModel):
    """Instrument data."""
    instrument_token: str
    exchange: str
    segment: str
    tradingsymbol: str
    name: str
    instrument_type: str
    tick_size: float
    lot_size: int
    expiry: Optional[datetime] = None
    strike: Optional[float] = None
    is_active: bool = True


class InstrumentResponse(BaseModel):
    """Response with instrument list."""
    instruments: List[InstrumentData]
    total: int


class HistoricalDataRequest(BaseModel):
    """Request for historical candle data."""
    instrument: str
    exchange: str
    interval: str = Field(..., pattern="^(1m|3m|5m|10m|15m|30m|60m|1d|1w|1M)$")
    from_date: str  # YYYY-MM-DD
    to_date: str    # YYYY-MM-DD
    continuous: bool = False


class CandleData(BaseModel):
    """OHLC candle data."""
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    oi: Optional[int] = None


class HistoricalDataResponse(BaseModel):
    """Response with historical data."""
    instrument: str
    exchange: str
    interval: str
    candles: List[CandleData]


class MarketStatusRequest(BaseModel):
    """Request for market status."""
    exchange: str = Field(default="NSE")


class MarketStatusData(BaseModel):
    """Market status data."""
    exchange: str
    status: str  # OPEN, CLOSED, PRE_OPEN, POST_CLOSE
    next_open: Optional[datetime] = None
    next_close: Optional[datetime] = None
    is_trading_day: bool


class MarketStatusResponse(BaseModel):
    """Market status response."""
    status: MarketStatusData


class IndicesData(BaseModel):
    """Index data."""
    name: str
    value: float
    change: float
    change_percent: float
    open: float
    high: float
    low: float
    previous_close: float
    timestamp: datetime


class IndicesResponse(BaseModel):
    """Indices response."""
    indices: List[IndicesData]


class OptionChainRequest(BaseModel):
    """Request for option chain."""
    underlying: str
    exchange: str
    expiry: Optional[str] = None


class OptionChainData(BaseModel):
    """Option chain data for a strike."""
    strike: float
    call_oi: int
    call_volume: int
    call_iv: float
    call_ltp: float
    call_change: float
    put_oi: int
    put_volume: int
    put_iv: float
    put_ltp: float
    put_change: float


class OptionChainResponse(BaseModel):
    """Option chain response."""
    underlying: str
    expiry: str
    spot_price: float
    strikes: List[OptionChainData]