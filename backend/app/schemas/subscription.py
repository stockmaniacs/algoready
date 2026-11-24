"""Subscription schemas."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class SubscriptionPlan(str):
    """Subscription plan types."""
    FREE = "free"
    PRO = "pro"
    PREMIUM = "premium"


class SubscriptionPlanDetails(BaseModel):
    """Subscription plan details."""
    name: str
    description: str
    price_monthly: float
    price_yearly: float
    features: List[str]
    strategy_limit: Optional[int] = None
    broker_limit: int
    signal_limit: Optional[int] = None
    api_access: bool
    paper_trading: bool
    backtesting: bool
    priority_support: bool


class SubscriptionBase(BaseModel):
    """Base subscription schema."""
    plan_type: str = Field(..., pattern="^(free|pro|premium)$")
    payment_id: Optional[str] = None
    status: str = Field(default="active", pattern="^(active|expired|cancelled|past_due)$")


class SubscriptionCreate(SubscriptionBase):
    """Schema for creating a subscription."""
    expires_at: Optional[datetime] = None


class SubscriptionUpdate(BaseModel):
    """Schema for updating a subscription."""
    plan_type: Optional[str] = None
    status: Optional[str] = None
    expires_at: Optional[datetime] = None
    payment_id: Optional[str] = None


class SubscriptionResponse(SubscriptionBase):
    """Schema for subscription response."""
    id: str
    user_id: str
    started_at: datetime
    expires_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class SubscriptionPlanInfo(BaseModel):
    """Available subscription plans."""
    free: SubscriptionPlanDetails
    pro: SubscriptionPlanDetails
    premium: SubscriptionPlanDetails


# Default plan configurations
DEFAULT_PLANS = {
    "free": SubscriptionPlanDetails(
        name="Free",
        description="Perfect for getting started with algorithmic trading",
        price_monthly=0,
        price_yearly=0,
        features=[
            "1 broker connection",
            "3 active strategies",
            "Basic signals",
            "Paper trading",
            "Community support"
        ],
        strategy_limit=3,
        broker_limit=1,
        signal_limit=50,
        api_access=False,
        paper_trading=True,
        backtesting=False,
        priority_support=False,
    ),
    "pro": SubscriptionPlanDetails(
        name="Pro",
        description="For active traders who need more power",
        price_monthly=999,
        price_yearly=9999,
        features=[
            "3 broker connections",
            "10 active strategies",
            "Advanced signals",
            "Paper & live trading",
            "Backtesting",
            "Email support"
        ],
        strategy_limit=10,
        broker_limit=3,
        signal_limit=500,
        api_access=True,
        paper_trading=True,
        backtesting=True,
        priority_support=False,
    ),
    "premium": SubscriptionPlanDetails(
        name="Premium",
        description="For professional traders and institutions",
        price_monthly=2999,
        price_yearly=29999,
        features=[
            "Unlimited broker connections",
            "Unlimited strategies",
            "Real-time signals",
            "Custom strategies",
            "Advanced backtesting",
            "Priority support",
            "API access",
            "Webhooks"
        ],
        strategy_limit=None,
        broker_limit=10,
        signal_limit=None,
        api_access=True,
        paper_trading=True,
        backtesting=True,
        priority_support=True,
    ),
}


class SubscriptionUpgradeRequest(BaseModel):
    """Request to upgrade subscription."""
    plan_type: str = Field(..., pattern="^(pro|premium)$")
    billing_cycle: str = Field(default="monthly", pattern="^(monthly|yearly)$")
    payment_method_id: Optional[str] = None


class SubscriptionCancelRequest(BaseModel):
    """Request to cancel subscription."""
    cancel_at_period_end: bool = True