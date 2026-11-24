"""Broker adapter base class and implementations."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
import httpx
import json


@dataclass
class BrokerCredentials:
    """Broker API credentials."""
    access_token: str
    refresh_token: Optional[str] = None
    expires_at: Optional[datetime] = None
    user_id: Optional[str] = None


@dataclass
class AccountInfo:
    """Broker account information."""
    user_id: str
    user_name: str
    email: str
    broker_type: str
    account_type: str
    balance: Optional[float] = None
    margin: Optional[float] = None


@dataclass
class PositionData:
    """Position data from broker."""
    instrument: str
    exchange: str
    direction: str  # LONG or SHORT
    quantity: float
    avg_entry_price: float
    current_price: float
    unrealized_pnl: float
    realized_pnl: float
    product_type: str


@dataclass
class OrderData:
    """Order data from broker."""
    instrument: str
    exchange: str
    transaction_type: str  # BUY or SELL
    order_type: str  # MARKET, LIMIT, SL, SLM
    product: str  # CNC, MIS, NRML, CO, BO
    quantity: float
    price: Optional[float]
    trigger_price: Optional[float]
    status: str
    broker_order_id: str
    filled_quantity: float
    average_price: Optional[float]
    placed_at: datetime


@dataclass
class HoldingData:
    """Holding data from broker."""
    instrument: str
    exchange: str
    quantity: float
    avg_price: float
    current_price: float
    pnl: float
    day_change: float
    day_change_percent: float


@dataclass
class QuoteData:
    """Quote data from broker."""
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
    oi: Optional[int] = None


@dataclass
class HistoricalCandle:
    """Historical candle data."""
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int


class BrokerAdapter(ABC):
    """Abstract base class for broker adapters."""
    
    def __init__(self, credentials: BrokerCredentials):
        self.credentials = credentials
        self.client = httpx.AsyncClient(timeout=30.0)
    
    @abstractmethod
    async def authenticate(self) -> bool:
        """Authenticate with broker API."""
        pass
    
    @abstractmethod
    async def get_account_info(self) -> AccountInfo:
        """Get account information."""
        pass
    
    @abstractmethod
    async def get_positions(self) -> List[PositionData]:
        """Get open positions."""
        pass
    
    @abstractmethod
    async def get_holdings(self) -> List[HoldingData]:
        """Get holdings (delivery positions)."""
        pass
    
    @abstractmethod
    async def get_orders(self, from_date: Optional[datetime] = None) -> List[OrderData]:
        """Get order history."""
        pass
    
    @abstractmethod
    async def place_order(self, order_params: Dict[str, Any]) -> OrderData:
        """Place a new order."""
        pass
    
    @abstractmethod
    async def modify_order(self, order_id: str, params: Dict[str, Any]) -> OrderData:
        """Modify an existing order."""
        pass
    
    @abstractmethod
    async def cancel_order(self, order_id: str) -> bool:
        """Cancel an order."""
        pass
    
    @abstractmethod
    async def get_quotes(self, instruments: List[str], exchange: str = "NSE") -> List[QuoteData]:
        """Get market quotes."""
        pass
    
    @abstractmethod
    async def get_historical_data(
        self,
        instrument: str,
        exchange: str,
        interval: str,
        from_date: str,
        to_date: str
    ) -> List[HistoricalCandle]:
        """Get historical candle data."""
        pass
    
    @abstractmethod
    async def search_instruments(self, query: str, exchange: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search for instruments."""
        pass
    
    @abstractmethod
    async def get_market_status(self, exchange: str = "NSE") -> Dict[str, Any]:
        """Get market status."""
        pass
    
    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()


class KiteAdapter(BrokerAdapter):
    """Zerodha Kite Connect adapter."""
    
    BASE_URL = "https://api.kite.trade"
    
    def __init__(self, credentials: BrokerCredentials):
        super().__init__(credentials)
        self.client.headers.update({
            "Authorization": f"token {self.credentials.access_token}",
            "Content-Type": "application/x-www-form-urlencoded",
        })
    
    async def authenticate(self) -> bool:
        """Validate Kite access token."""
        try:
            response = await self.client.get(f"{self.BASE_URL}/user/profile")
            return response.status_code == 200
        except Exception:
            return False
    
    async def get_account_info(self) -> AccountInfo:
        """Get Kite user profile."""
        response = await self.client.get(f"{self.BASE_URL}/user/profile")
        data = response.json()["data"]
        
        # Get margins
        margins_response = await self.client.get(f"{self.BASE_URL}/user/margins")
        margins_data = margins_response.json()["data"]["equity"]
        
        return AccountInfo(
            user_id=data["user_id"],
            user_name=data["user_name"],
            email=data["email"],
            broker_type="zerodha",
            account_type="equity",
            balance=margins_data.get("available", {}).get("cash"),
            margin=margins_data.get("available", {}).get("margin"),
        )
    
    async def get_positions(self) -> List[PositionData]:
        """Get Kite positions."""
        response = await self.client.get(f"{self.BASE_URL}/portfolio/positions")
        data = response.json()["data"]
        
        positions = []
        for pos in data.get("net", []):
            if pos["quantity"] != 0:
                positions.append(PositionData(
                    instrument=pos["tradingsymbol"],
                    exchange=pos["exchange"],
                    direction="LONG" if pos["quantity"] > 0 else "SHORT",
                    quantity=abs(pos["quantity"]),
                    avg_entry_price=pos["average_price"],
                    current_price=pos["last_price"],
                    unrealized_pnl=pos["unrealised"],
                    realized_pnl=pos["realised"],
                    product_type=pos["product"],
                ))
        return positions
    
    async def get_holdings(self) -> List[HoldingData]:
        """Get Kite holdings."""
        response = await self.client.get(f"{self.BASE_URL}/portfolio/holdings")
        data = response.json()["data"]
        
        holdings = []
        for h in data:
            holdings.append(HoldingData(
                instrument=h["tradingsymbol"],
                exchange=h["exchange"],
                quantity=h["quantity"],
                avg_price=h["average_price"],
                current_price=h["last_price"],
                pnl=h["pnl"],
                day_change=h["day_change"],
                day_change_percent=h["day_change_percentage"],
            ))
        return holdings
    
    async def get_orders(self, from_date: Optional[datetime] = None) -> List[OrderData]:
        """Get Kite order history."""
        response = await self.client.get(f"{self.BASE_URL}/orders")
        data = response.json()["data"]
        
        orders = []
        for o in data:
            orders.append(OrderData(
                instrument=o["tradingsymbol"],
                exchange=o["exchange"],
                transaction_type=o["transaction_type"],
                order_type=o["order_type"],
                product=o["product"],
                quantity=o["quantity"],
                price=o["price"] if o["price"] > 0 else None,
                trigger_price=o["trigger_price"] if o["trigger_price"] > 0 else None,
                status=o["status"],
                broker_order_id=o["order_id"],
                filled_quantity=o["filled_quantity"],
                average_price=o["average_price"] if o["average_price"] > 0 else None,
                placed_at=datetime.fromisoformat(o["order_timestamp"].replace("Z", "+00:00")),
            ))
        return orders
    
    async def place_order(self, order_params: Dict[str, Any]) -> OrderData:
        """Place order via Kite."""
        response = await self.client.post(
            f"{self.BASE_URL}/orders/regular",
            data=order_params
        )
        data = response.json()["data"]
        
        # Get the placed order details
        order_response = await self.client.get(f"{self.BASE_URL}/orders")
        orders = order_response.json()["data"]
        
        # Find the newly placed order
        new_order = next((o for o in orders if o["order_id"] == data["order_id"]), None)
        
        if new_order:
            return OrderData(
                instrument=new_order["tradingsymbol"],
                exchange=new_order["exchange"],
                transaction_type=new_order["transaction_type"],
                order_type=new_order["order_type"],
                product=new_order["product"],
                quantity=new_order["quantity"],
                price=new_order["price"] if new_order["price"] > 0 else None,
                trigger_price=new_order["trigger_price"] if new_order["trigger_price"] > 0 else None,
                status=new_order["status"],
                broker_order_id=new_order["order_id"],
                filled_quantity=new_order["filled_quantity"],
                average_price=new_order["average_price"] if new_order["average_price"] > 0 else None,
                placed_at=datetime.fromisoformat(new_order["order_timestamp"].replace("Z", "+00:00")),
            )
        
        raise Exception("Failed to retrieve placed order")
    
    async def modify_order(self, order_id: str, params: Dict[str, Any]) -> OrderData:
        """Modify Kite order."""
        response = await self.client.put(
            f"{self.BASE_URL}/orders/regular/{order_id}",
            data=params
        )
        data = response.json()["data"]
        
        # Get updated order
        order_response = await self.client.get(f"{self.BASE_URL}/orders")
        orders = order_response.json()["data"]
        updated_order = next((o for o in orders if o["order_id"] == order_id), None)
        
        if updated_order:
            return OrderData(
                instrument=updated_order["tradingsymbol"],
                exchange=updated_order["exchange"],
                transaction_type=updated_order["transaction_type"],
                order_type=updated_order["order_type"],
                product=updated_order["product"],
                quantity=updated_order["quantity"],
                price=updated_order["price"] if updated_order["price"] > 0 else None,
                trigger_price=updated_order["trigger_price"] if updated_order["trigger_price"] > 0 else None,
                status=updated_order["status"],
                broker_order_id=updated_order["order_id"],
                filled_quantity=updated_order["filled_quantity"],
                average_price=updated_order["average_price"] if updated_order["average_price"] > 0 else None,
                placed_at=datetime.fromisoformat(updated_order["order_timestamp"].replace("Z", "+00:00")),
            )
        
        raise Exception("Failed to retrieve modified order")
    
    async def cancel_order(self, order_id: str) -> bool:
        """Cancel Kite order."""
        response = await self.client.delete(f"{self.BASE_URL}/orders/regular/{order_id}")
        return response.status_code == 200
    
    async def get_quotes(self, instruments: List[str], exchange: str = "NSE") -> List[QuoteData]:
        """Get quotes from Kite."""
        # Format instruments for Kite API
        formatted = [f"{exchange}:{inst}" for inst in instruments]
        
        response = await self.client.get(
            f"{self.BASE_URL}/quote/ltp",
            params={"i": ",".join(formatted)}
        )
        data = response.json()["data"]
        
        quotes = []
        for inst in formatted:
            if inst in data:
                q = data[inst]
                quotes.append(QuoteData(
                    instrument=inst.split(":")[1],
                    exchange=inst.split(":")[0],
                    last_price=q["last_price"],
                    change=q.get("change", 0),
                    change_percent=q.get("change_percent", 0),
                    open=q.get("ohlc", {}).get("open", 0),
                    high=q.get("ohlc", {}).get("high", 0),
                    low=q.get("ohlc", {}).get("low", 0),
                    close=q.get("ohlc", {}).get("close", 0),
                    volume=q.get("volume", 0),
                    oi=q.get("oi"),
                ))
        return quotes
    
    async def get_historical_data(
        self,
        instrument: str,
        exchange: str,
        interval: str,
        from_date: str,
        to_date: str
    ) -> List[HistoricalCandle]:
        """Get historical data from Kite."""
        # Note: Kite requires instrument token, not symbol
        # This would need a symbol-to-token mapping
        params = {
            "from": from_date,
            "to": to_date,
            "interval": interval,
        }
        
        response = await self.client.get(
            f"{self.BASE_URL}/instruments/historical/{instrument}/{exchange}",
            params=params
        )
        data = response.json()["data"]["candles"]
        
        candles = []
        for c in data:
            candles.append(HistoricalCandle(
                timestamp=datetime.fromisoformat(c[0].replace("Z", "+00:00")),
                open=c[1],
                high=c[2],
                low=c[3],
                close=c[4],
                volume=c[5],
            ))
        return candles
    
    async def search_instruments(self, query: str, exchange: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search instruments on Kite."""
        # Download instruments file if not cached
        # This is a simplified version
        params = {"exchange": exchange} if exchange else {}
        response = await self.client.get(f"{self.BASE_URL}/instruments", params=params)
        instruments = response.text.strip().split("\n")
        
        # Parse CSV
        results = []
        for line in instruments[1:]:  # Skip header
            parts = line.split(",")
            if len(parts) >= 12:
                tradingsymbol = parts[2]
                if query.upper() in tradingsymbol.upper():
                    results.append({
                        "instrument_token": parts[0],
                        "exchange": parts[1],
                        "tradingsymbol": tradingsymbol,
                        "name": parts[3],
                        "instrument_type": parts[5],
                        "tick_size": float(parts[6]),
                        "lot_size": int(parts[7]),
                    })
        return results[:20]
    
    async def get_market_status(self, exchange: str = "NSE") -> Dict[str, Any]:
        """Get market status from Kite."""
        response = await self.client.get(f"{self.BASE_URL}/market/status")
        return response.json()["data"]


class UpstoxAdapter(BrokerAdapter):
    """Upstox API adapter."""
    
    BASE_URL = "https://api.upstox.com/v2"
    
    def __init__(self, credentials: BrokerCredentials):
        super().__init__(credentials)
        self.client.headers.update({
            "Authorization": f"Bearer {self.credentials.access_token}",
            "Accept": "application/json",
        })
    
    async def authenticate(self) -> bool:
        """Validate Upstox access token."""
        try:
            response = await self.client.get(f"{self.BASE_URL}/user/profile")
            return response.status_code == 200
        except Exception:
            return False
    
    async def get_account_info(self) -> AccountInfo:
        """Get Upstox user profile."""
        response = await self.client.get(f"{self.BASE_URL}/user/profile")
        data = response.json()["data"]
        
        # Get funds
        funds_response = await self.client.get(f"{self.BASE_URL}/user/funds")
        funds_data = funds_response.json()["data"]
        
        return AccountInfo(
            user_id=data["user_id"],
            user_name=data["name"],
            email=data["email"],
            broker_type="upstox",
            account_type="equity",
            balance=funds_data.get("equity", {}).get("available_balance"),
            margin=funds_data.get("equity", {}).get("used_margin"),
        )
    
    async def get_positions(self) -> List[PositionData]:
        """Get Upstox positions."""
        response = await self.client.get(f"{self.BASE_URL}/portfolio/short-term-positions")
        data = response.json()["data"]
        
        positions = []
        for pos in data:
            if pos["quantity"] != 0:
                positions.append(PositionData(
                    instrument=pos["tradingsymbol"],
                    exchange=pos["exchange"],
                    direction="LONG" if pos["quantity"] > 0 else "SHORT",
                    quantity=abs(pos["quantity"]),
                    avg_entry_price=pos["average_price"],
                    current_price=pos["last_price"],
                    unrealized_pnl=pos["unrealized_profit"],
                    realized_pnl=pos["realized_profit"],
                    product_type=pos["product"],
                ))
        return positions
    
    async def get_holdings(self) -> List[HoldingData]:
        """Get Upstox holdings."""
        response = await self.client.get(f"{self.BASE_URL}/portfolio/long-term-holdings")
        data = response.json()["data"]
        
        holdings = []
        for h in data:
            holdings.append(HoldingData(
                instrument=h["tradingsymbol"],
                exchange=h["exchange"],
                quantity=h["quantity"],
                avg_price=h["average_price"],
                current_price=h["last_price"],
                pnl=h["pnl"],
                day_change=h["day_change"],
                day_change_percent=h["day_change_percentage"],
            ))
        return holdings
    
    async def get_orders(self, from_date: Optional[datetime] = None) -> List[OrderData]:
        """Get Upstox order history."""
        params = {}
        if from_date:
            params["from_date"] = from_date.strftime("%Y-%m-%d")
        
        response = await self.client.get(f"{self.BASE_URL}/order/retrieve-all", params=params)
        data = response.json()["data"]
        
        orders = []
        for o in data:
            orders.append(OrderData(
                instrument=o["tradingsymbol"],
                exchange=o["exchange"],
                transaction_type=o["transaction_type"],
                order_type=o["order_type"],
                product=o["product"],
                quantity=o["quantity"],
                price=o["price"] if o["price"] > 0 else None,
                trigger_price=o["trigger_price"] if o["trigger_price"] > 0 else None,
                status=o["status"],
                broker_order_id=o["order_id"],
                filled_quantity=o["filled_quantity"],
                average_price=o["average_price"] if o["average_price"] > 0 else None,
                placed_at=datetime.fromisoformat(o["order_timestamp"].replace("Z", "+00:00")),
            ))
        return orders
    
    async def place_order(self, order_params: Dict[str, Any]) -> OrderData:
        """Place order via Upstox."""
        response = await self.client.post(
            f"{self.BASE_URL}/order/place",
            json=order_params
        )
        data = response.json()["data"]
        
        # Get order details
        order_response = await self.client.get(f"{self.BASE_URL}/order/details", params={"order_id": data["order_id"]})
        order_data = order_response.json()["data"]
        
        return OrderData(
            instrument=order_data["tradingsymbol"],
            exchange=order_data["exchange"],
            transaction_type=order_data["transaction_type"],
            order_type=order_data["order_type"],
            product=order_data["product"],
            quantity=order_data["quantity"],
            price=order_data["price"] if order_data["price"] > 0 else None,
            trigger_price=order_data["trigger_price"] if order_data["trigger_price"] > 0 else None,
            status=order_data["status"],
            broker_order_id=order_data["order_id"],
            filled_quantity=order_data["filled_quantity"],
            average_price=order_data["average_price"] if order_data["average_price"] > 0 else None,
            placed_at=datetime.fromisoformat(order_data["order_timestamp"].replace("Z", "+00:00")),
        )
    
    async def modify_order(self, order_id: str, params: Dict[str, Any]) -> OrderData:
        """Modify Upstox order."""
        response = await self.client.put(
            f"{self.BASE_URL}/order/modify",
            json={"order_id": order_id, **params}
        )
        data = response.json()["data"]
        
        # Get updated order
        order_response = await self.client.get(f"{self.BASE_URL}/order/details", params={"order_id": order_id})
        updated_order = order_response.json()["data"]
        
        return OrderData(
            instrument=updated_order["tradingsymbol"],
            exchange=updated_order["exchange"],
            transaction_type=updated_order["transaction_type"],
            order_type=updated_order["order_type"],
            product=updated_order["product"],
            quantity=updated_order["quantity"],
            price=updated_order["price"] if updated_order["price"] > 0 else None,
            trigger_price=updated_order["trigger_price"] if updated_order["trigger_price"] > 0 else None,
            status=updated_order["status"],
            broker_order_id=updated_order["order_id"],
            filled_quantity=updated_order["filled_quantity"],
            average_price=updated_order["average_price"] if updated_order["average_price"] > 0 else None,
            placed_at=datetime.fromisoformat(updated_order["order_timestamp"].replace("Z", "+00:00")),
        )
    
    async def cancel_order(self, order_id: str) -> bool:
        """Cancel Upstox order."""
        response = await self.client.delete(f"{self.BASE_URL}/order/cancel", params={"order_id": order_id})
        return response.status_code == 200
    
    async def get_quotes(self, instruments: List[str], exchange: str = "NSE") -> List[QuoteData]:
        """Get quotes from Upstox."""
        formatted = [f"{exchange}_EQ|{inst}" for inst in instruments]
        
        response = await self.client.get(
            f"{self.BASE_URL}/market-quote/ltp",
            params={"instrument_key": ",".join(formatted)}
        )
        data = response.json()["data"]
        
        quotes = []
        for inst in formatted:
            if inst in data:
                q = data[inst]
                quotes.append(QuoteData(
                    instrument=inst.split("|")[1],
                    exchange=exchange,
                    last_price=q["last_price"],
                    change=q.get("net_change", 0),
                    change_percent=q.get("percent_change", 0),
                    open=q.get("ohlc", {}).get("open", 0),
                    high=q.get("ohlc", {}).get("high", 0),
                    low=q.get("ohlc", {}).get("low", 0),
                    close=q.get("ohlc", {}).get("close", 0),
                    volume=q.get("volume", 0),
                    oi=q.get("oi"),
                ))
        return quotes
    
    async def get_historical_data(
        self,
        instrument: str,
        exchange: str,
        interval: str,
        from_date: str,
        to_date: str
    ) -> List[HistoricalCandle]:
        """Get historical data from Upstox."""
        # Upstox uses instrument keys
        instrument_key = f"{exchange}_EQ|{instrument}"
        
        params = {
            "interval": interval,
            "from": from_date,
            "to": to_date,
        }
        
        response = await self.client.get(
            f"{self.BASE_URL}/historical-candle/{instrument_key}",
            params=params
        )
        data = response.json()["data"]["candles"]
        
        candles = []
        for c in data:
            candles.append(HistoricalCandle(
                timestamp=datetime.fromisoformat(c[0].replace("Z", "+00:00")),
                open=c[1],
                high=c[2],
                low=c[3],
                close=c[4],
                volume=c[5],
            ))
        return candles
    
    async def search_instruments(self, query: str, exchange: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search instruments on Upstox."""
        # Upstox doesn't have a direct search endpoint
        # Would need to download master contract
        return []
    
    async def get_market_status(self, exchange: str = "NSE") -> Dict[str, Any]:
        """Get market status from Upstox."""
        response = await self.client.get(f"{self.BASE_URL}/market/status")
        return response.json()["data"]


class FyersAdapter(BrokerAdapter):
    """FYERS API adapter."""
    
    BASE_URL = "https://api.fyers.in/api/v3"
    
    def __init__(self, credentials: BrokerCredentials):
        super().__init__(credentials)
        self.client.headers.update({
            "Authorization": f"Bearer {self.credentials.access_token}",
            "Content-Type": "application/json",
        })
    
    async def authenticate(self) -> bool:
        """Validate FYERS access token."""
        try:
            response = await self.client.get(f"{self.BASE_URL}/profile")
            return response.status_code == 200
        except Exception:
            return False
    
    async def get_account_info(self) -> AccountInfo:
        """Get FYERS user profile."""
        response = await self.client.get(f"{self.BASE_URL}/profile")
        data = response.json()["data"]
        
        # Get funds
        funds_response = await self.client.get(f"{self.BASE_URL}/funds")
        funds_data = funds_response.json()["data"]
        
        return AccountInfo(
            user_id=data["fy_id"],
            user_name=data["name"],
            email=data["email_id"],
            broker_type="fyers",
            account_type="equity",
            balance=funds_data.get("available_balance"),
            margin=funds_data.get("margin"),
        )
    
    async def get_positions(self) -> List[PositionData]:
        """Get FYERS positions."""
        response = await self.client.get(f"{self.BASE_URL}/positions")
        data = response.json()["data"]
        
        positions = []
        for pos in data.get("netPositions", []):
            if pos["qty"] != 0:
                positions.append(PositionData(
                    instrument=pos["symbol"].split(":")[-1],
                    exchange=pos["symbol"].split(":")[0],
                    direction="LONG" if pos["qty"] > 0 else "SHORT",
                    quantity=abs(pos["qty"]),
                    avg_entry_price=pos["avgPrice"],
                    current_price=pos["curPrice"],
                    unrealized_pnl=pos["unrealized_profit"],
                    realized_pnl=pos["realized_profit"],
                    product_type=pos["productType"],
                ))
        return positions
    
    async def get_holdings(self) -> List[HoldingData]:
        """Get FYERS holdings."""
        response = await self.client.get(f"{self.BASE_URL}/holdings")
        data = response.json()["data"]
        
        holdings = []
        for h in data:
            holdings.append(HoldingData(
                instrument=h["symbol"].split(":")[-1],
                exchange=h["symbol"].split(":")[0],
                quantity=h["qty"],
                avg_price=h["avgPrice"],
                current_price=h["curPrice"],
                pnl=h["pl"],
                day_change=h["dayChange"],
                day_change_percent=h["dayChangePerc"],
            ))
        return holdings
    
    async def get_orders(self, from_date: Optional[datetime] = None) -> List[OrderData]:
        """Get FYERS order history."""
        params = {}
        if from_date:
            params["from_date"] = from_date.strftime("%Y-%m-%d")
        
        response = await self.client.get(f"{self.BASE_URL}/orders", params=params)
        data = response.json()["data"]
        
        orders = []
        for o in data:
            orders.append(OrderData(
                instrument=o["symbol"].split(":")[-1],
                exchange=o["symbol"].split(":")[0],
                transaction_type=o["side"],
                order_type=o["type"],
                product=o["productType"],
                quantity=o["qty"],
                price=o["limitPrice"] if o["limitPrice"] > 0 else None,
                trigger_price=o["stopPrice"] if o["stopPrice"] > 0 else None,
                status=o["status"],
                broker_order_id=o["id"],
                filled_quantity=o["filledQty"],
                average_price=o["avgPrice"] if o["avgPrice"] > 0 else None,
                placed_at=datetime.fromisoformat(o["orderDateTime"].replace("Z", "+00:00")),
            ))
        return orders
    
    async def place_order(self, order_params: Dict[str, Any]) -> OrderData:
        """Place order via FYERS."""
        response = await self.client.post(
            f"{self.BASE_URL}/orders",
            json=order_params
        )
        data = response.json()["data"]
        
        # Get order details
        order_response = await self.client.get(f"{self.BASE_URL}/orders", params={"id": data["id"]})
        order_data = order_response.json()["data"][0]
        
        return OrderData(
            instrument=order_data["symbol"].split(":")[-1],
            exchange=order_data["symbol"].split(":")[0],
            transaction_type=order_data["side"],
            order_type=order_data["type"],
            product=order_data["productType"],
            quantity=order_data["qty"],
            price=order_data["limitPrice"] if order_data["limitPrice"] > 0 else None,
            trigger_price=order_data["stopPrice"] if order_data["stopPrice"] > 0 else None,
            status=order_data["status"],
            broker_order_id=order_data["id"],
            filled_quantity=order_data["filledQty"],
            average_price=order_data["avgPrice"] if order_data["avgPrice"] > 0 else None,
            placed_at=datetime.fromisoformat(order_data["orderDateTime"].replace("Z", "+00:00")),
        )
    
    async def modify_order(self, order_id: str, params: Dict[str, Any]) -> OrderData:
        """Modify FYERS order."""
        response = await self.client.put(
            f"{self.BASE_URL}/orders/{order_id}",
            json=params
        )
        data = response.json()["data"]
        
        # Get updated order
        order_response = await self.client.get(f"{self.BASE_URL}/orders", params={"id": order_id})
        updated_order = order_response.json()["data"][0]
        
        return OrderData(
            instrument=updated_order["symbol"].split(":")[-1],
            exchange=updated_order["symbol"].split(":")[0],
            transaction_type=updated_order["side"],
            order_type=updated_order["type"],
            product=updated_order["productType"],
            quantity=updated_order["qty"],
            price=updated_order["limitPrice"] if updated_order["limitPrice"] > 0 else None,
            trigger_price=updated_order["stopPrice"] if updated_order["stopPrice"] > 0 else None,
            status=updated_order["status"],
            broker_order_id=updated_order["id"],
            filled_quantity=updated_order["filledQty"],
            average_price=updated_order["avgPrice"] if updated_order["avgPrice"] > 0 else None,
            placed_at=datetime.fromisoformat(updated_order["orderDateTime"].replace("Z", "+00:00")),
        )
    
    async def cancel_order(self, order_id: str) -> bool:
        """Cancel FYERS order."""
        response = await self.client.delete(f"{self.BASE_URL}/orders/{order_id}")
        return response.status_code == 200
    
    async def get_quotes(self, instruments: List[str], exchange: str = "NSE") -> List[QuoteData]:
        """Get quotes from FYERS."""
        formatted = [f"{exchange}:{inst}" for inst in instruments]
        
        response = await self.client.get(
            f"{self.BASE_URL}/quotes",
            params={"symbols": ",".join(formatted)}
        )
        data = response.json()["data"]
        
        quotes = []
        for d in data:
            quotes.append(QuoteData(
                instrument=d["symbol"].split(":")[-1],
                exchange=d["symbol"].split(":")[0],
                last_price=d["v"]["lp"],
                change=d["v"]["ch"],
                change_percent=d["v"]["chp"],
                open=d["v"]["o"],
                high=d["v"]["h"],
                low=d["v"]["l"],
                close=d["v"]["c"],
                volume=d["v"]["v"],
                oi=d["v"].get("oi"),
            ))
        return quotes
    
    async def get_historical_data(
        self,
        instrument: str,
        exchange: str,
        interval: str,
        from_date: str,
        to_date: str
    ) -> List[HistoricalCandle]:
        """Get historical data from FYERS."""
        symbol = f"{exchange}:{instrument}"
        
        params = {
            "symbol": symbol,
            "resolution": interval,
            "date_format": "1",
            "range_from": from_date,
            "range_to": to_date,
            "cont_flag": "1",
        }
        
        response = await self.client.get(f"{self.BASE_URL}/history", params=params)
        data = response.json()["candles"]
        
        candles = []
        for c in data:
            candles.append(HistoricalCandle(
                timestamp=datetime.fromtimestamp(c[0]),
                open=c[1],
                high=c[2],
                low=c[3],
                close=c[4],
                volume=c[5],
            ))
        return candles
    
    async def search_instruments(self, query: str, exchange: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search instruments on FYERS."""
        # FYERS doesn't have a direct search endpoint
        return []
    
    async def get_market_status(self, exchange: str = "NSE") -> Dict[str, Any]:
        """Get market status from FYERS."""
        # FYERS doesn't have a market status endpoint
        return {"status": "UNKNOWN"}


def get_broker_adapter(broker_type: str, credentials: BrokerCredentials) -> BrokerAdapter:
    """Factory function to get broker adapter."""
    adapters = {
        "zerodha": KiteAdapter,
        "upstox": UpstoxAdapter,
        "fyers": FyersAdapter,
    }
    
    if broker_type not in adapters:
        raise ValueError(f"Unsupported broker type: {broker_type}")
    
    return adapters[broker_type](credentials)