"""Market data routes for AlgoReady."""

from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

router = APIRouter()


class QuoteResponse(BaseModel):
    """Market quote response."""
    instrument: str
    exchange: str
    symbol: str
    ltp: float
    change: float
    change_percent: float
    volume: int
    oi: int  # Open Interest for options
    date: str


class HistoricalCandle(BaseModel):
    """Historical candle data."""
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int


class HistoricalDataResponse(BaseModel):
    """Historical data response."""
    instrument: str
    exchange: str
    timeframe: str
    candles: List[HistoricalCandle]


class InstrumentResponse(BaseModel):
    """Instrument metadata."""
    instrument_token: int
    trading_symbol: str
    exchange: str
    instrument_type: str
    name: str
    expiry_date: Optional[str] = None
    strike_price: Optional[float] = None
    option_type: Optional[str] = None
    lot_size: int
    tick_size: float
    multiplier: int


@router.get("/quotes", response_model=List[QuoteResponse])
async def get_quotes(
    instruments: str = Query(..., description="Comma-separated list of instruments"),
    broker: Optional[str] = Query(None)
):
    """Get quotes for multiple instruments."""
    # TODO: Implement with broker integration
    instrument_list = instruments.split(',')[:10]  # Limit to 10
    quotes = []
    for inst in instrument_list:
        quotes.append(QuoteResponse(
            instrument=inst,
            exchange="NSE",
            symbol=inst,
            ltp=100.0,
            change=0.5,
            change_percent=0.5,
            volume=10000,
            oi=0,
            date=datetime.now().strftime("%Y-%m-%d")
        ))
    return quotes


@router.get("/quotes/{instrument}", response_model=QuoteResponse)
async def get_quote(instrument: str, broker: Optional[str] = Query(None)):
    """Get quote for a single instrument."""
    return QuoteResponse(
        instrument=instrument,
        exchange="NSE",
        symbol=instrument,
        ltp=100.0,
        change=0.5,
        change_percent=0.5,
        volume=10000,
        oi=0,
        date=datetime.now().strftime("%Y-%m-%d")
    )


@router.get("/history", response_model=HistoricalDataResponse)
async def get_historical_data(
    instrument: str,
    timeframe: str = "15m",
    from_date: datetime = Query(...),
    to_date: datetime = Query(...),
    broker: Optional[str] = Query(None)
):
    """Get historical candle data."""
    candles = []
    for i in range(100):
        candles.append(HistoricalCandle(
            timestamp=datetime.now(),
            open=99.0 + i * 0.1,
            high=100.0 + i * 0.1,
            low=99.0 + i * 0.05,
            close=99.5 + i * 0.1,
            volume=10000 + i * 100
        ))
    
    return HistoricalDataResponse(
        instrument=instrument,
        exchange="NSE",
        timeframe=timeframe,
        candles=candles
    )


@router.get("/instruments", response_model=List[InstrumentResponse])
async def search_instruments(
    query: str = Query(..., min_length=1),
    exchange: Optional[str] = Query(None)
):
    """Search for instruments by symbol or name."""
    return [
        InstrumentResponse(
            instrument_token=12345,
            trading_symbol=query.upper(),
            exchange=exchange or "NSE",
            instrument_type="EQ",
            name=f"{query.upper()} Ltd",
            lot_size=1,
            tick_size=0.05,
            multiplier=1
        )
    ]