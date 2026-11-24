"""Strategy routes for AlgoReady."""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

router = APIRouter()


class StrategyCategory(str, Enum):
    scalping = "scalping"
    breakout = "breakout"
    momentum = "momentum"
    trend_following = "trend_following"
    mean_reversion = "mean_reversion"
    intraday = "intraday"
    swing = "swing"
    options = "options"


class StrategyResponse(BaseModel):
    """Response model for strategy listing."""
    id: str
    name: str
    description: str
    category: StrategyCategory
    market: str  # 'india_stocks', 'crypto', 'us_stocks'
    instrument_filter: Optional[str] = None
    timeframe: str
    entry_rules: str
    exit_rules: str
    target_percent: float
    stop_loss_percent: float
    risk_per_trade: float
    backtest_metrics: Optional[dict] = None
    created_by: Optional[str] = None
    is_public: bool = True
    subscription_required: bool = False


class StrategyDetailResponse(StrategyResponse):
    """Detailed strategy response."""
    parameters: dict
    entry_conditions: List[str]
    exit_conditions: List[str]
    performance_metrics: Optional[dict] = None
    last_updated: datetime


@router.get("/", response_model=List[StrategyResponse])
async def list_strategies(
    category: Optional[StrategyCategory] = Query(None),
    market: Optional[str] = Query(None),
    limit: int = Query(100, le=100)
):
    """List available strategies."""
    # TODO: Implement with database
    sample_strategies = [
        StrategyResponse(
            id="strat_1",
            name="EMA Cross",
            description="Simple EMA crossover strategy for trend following",
            category=StrategyCategory.trend_following,
            market="india_stocks",
            timeframe="15m",
            entry_rules="Buy when 9 EMA crosses above 21 EMA",
            exit_rules="Exit when 9 EMA crosses below 21 EMA",
            target_percent=2.0,
            stop_loss_percent=1.5,
            risk_per_trade=1.0
        ),
        StrategyResponse(
            id="strat_2",
            name="Mean Reversion BB",
            description="Bollinger Bands mean reversion for volatile markets",
            category=StrategyCategory.mean_reversion,
            market="india_stocks",
            timeframe="5m",
            entry_rules="Buy when price touches lower Bollinger Band",
            exit_rules="Exit at middle band or stop loss",
            target_percent=1.5,
            stop_loss_percent=2.0,
            risk_per_trade=0.5
        )
    ]
    return sample_strategies


@router.get("/{strategy_id}", response_model=StrategyDetailResponse)
async def get_strategy(strategy_id: str):
    """Get detailed strategy information."""
    return StrategyDetailResponse(
        id=strategy_id,
        name="EMA Cross",
        description="Simple EMA crossover strategy for trend following",
        category=StrategyCategory.trend_following,
        market="india_stocks",
        timeframe="15m",
        entry_rules="Buy when 9 EMA crosses above 21 EMA",
        exit_rules="Exit when 9 EMA crosses below 21 EMA",
        target_percent=2.0,
        stop_loss_percent=1.5,
        risk_per_trade=1.0,
        parameters={
            "fast_ema_period": 9,
            "slow_ema_period": 21,
            "min_volume": 100
        },
        entry_conditions=[
            "Price above 50-period SMA",
            "9 EMA crosses above 21 EMA on candle close",
            "Volume above average"
        ],
        exit_conditions=[
            "9 EMA crosses below 21 EMA",
            "Stop loss hit",
            "Target price reached",
            "End of session"
        ]
    )


@router.post("/{strategy_id}/apply")
async def apply_strategy(strategy_id: str, broker_id: str):
    """Apply strategy to a chart or instrument."""
    return {
        "message": f"Strategy {strategy_id} applied successfully",
        "strategy_id": strategy_id,
        "broker_id": broker_id
    }


@router.delete("/user-strategies/{user_strategy_id}")
async def unapply_strategy(user_strategy_id: str):
    """Remove applied strategy."""
    return {"message": "Strategy removed successfully"}