"""Strategy schemas."""

from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, ConfigDict


class StrategyCategory(str):
    """Strategy categories."""
    SCALPING = "scalping"
    MOMENTUM = "momentum"
    SWING = "swing"
    BREAKOUT = "breakout"
    REVERSION = "reversion"
    ARBITRAGE = "arbitrage"
    OPTIONS = "options"
    CUSTOM = "custom"


class StrategyBase(BaseModel):
    """Base strategy schema."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category: str = Field(..., pattern="^(scalping|momentum|swing|breakout|reversion|arbitrage|options|custom)$")
    market: str = Field(default="india_stocks")
    instrument_filter: Optional[Dict[str, Any]] = None
    timeframe: str = Field(default="15m")
    parameters: Optional[Dict[str, Any]] = None
    entry_rules: Optional[Dict[str, Any]] = None
    exit_rules: Optional[Dict[str, Any]] = None
    target_percent: int = Field(..., ge=1, le=1000)
    stop_loss_percent: int = Field(..., ge=1, le=100)
    risk_per_trade: int = Field(..., ge=1, le=100)
    subscription_required: bool = False


class StrategyCreate(StrategyBase):
    """Schema for creating a strategy."""
    pass


class StrategyUpdate(BaseModel):
    """Schema for updating a strategy."""
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    market: Optional[str] = None
    instrument_filter: Optional[Dict[str, Any]] = None
    timeframe: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    entry_rules: Optional[Dict[str, Any]] = None
    exit_rules: Optional[Dict[str, Any]] = None
    target_percent: Optional[int] = None
    stop_loss_percent: Optional[int] = None
    risk_per_trade: Optional[int] = None
    backtest_metrics: Optional[Dict[str, Any]] = None
    is_public: Optional[bool] = None
    subscription_required: Optional[bool] = None
    version: Optional[str] = None


class StrategyResponse(StrategyBase):
    """Schema for strategy response."""
    id: str
    slug: Optional[str] = None
    created_by: Optional[str] = None
    is_public: bool
    backtest_metrics: Optional[Dict[str, Any]] = None
    version: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class StrategyList(BaseModel):
    """Paginated strategy list."""
    strategies: List[StrategyResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class StrategyApplyRequest(BaseModel):
    """Request to apply a strategy."""
    strategy_id: str
    broker_connection_id: Optional[str] = None
    configuration: Optional[Dict[str, Any]] = None


class StrategyBacktestRequest(BaseModel):
    """Request to backtest a strategy."""
    strategy_id: str
    start_date: str
    end_date: str
    initial_capital: float = 100000
    commission: float = 0.0003
    slippage: float = 0.0001


class StrategyBacktestResponse(BaseModel):
    """Backtest results."""
    strategy_id: str
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    total_pnl: float
    max_drawdown: float
    sharpe_ratio: float
    sortino_ratio: float
    profit_factor: float
    avg_win: float
    avg_loss: float
    max_win: float
    max_loss: float
    trades: List[Dict[str, Any]]
    equity_curve: List[Dict[str, Any]]