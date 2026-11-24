"""Signal generator service for creating trading signals from strategies."""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
import asyncio
import uuid

from app.services.strategy_engine import StrategyEngine, StrategyConfig, Signal
from app.services.broker_adapter import BrokerAdapter, get_broker_adapter, BrokerCredentials
from app.db.base import get_db
from app.models.signal import Signal as SignalModel
from app.models.strategy import Strategy as StrategyModel
from app.models.user_strategy import UserStrategy
from app.models.broker_connection import BrokerConnection


@dataclass
class MarketData:
    """Market data container."""
    instrument: str
    exchange: str
    candles: List[Dict[str, Any]]


class SignalGenerator:
    """Service for generating and managing trading signals."""
    
    def __init__(self):
        self.engine = StrategyEngine()
        self.active_generators: Dict[str, asyncio.Task] = {}
        self.market_data_cache: Dict[str, MarketData] = {}
    
    async def generate_signals_for_user(
        self,
        user_id: str,
        broker_connection_id: Optional[str] = None,
    ) -> List[SignalModel]:
        """Generate signals for all active user strategies."""
        db = next(get_db())
        
        try:
            # Get user's active strategies
            user_strategies = db.query(UserStrategy).filter(
                UserStrategy.user_id == user_id,
                UserStrategy.is_active == True
            ).all()
            
            if not user_strategies:
                return []
            
            # Get broker connection for market data
            if broker_connection_id:
                broker_conn = db.query(BrokerConnection).filter(
                    BrokerConnection.id == broker_connection_id,
                    BrokerConnection.user_id == user_id
                ).first()
            else:
                broker_conn = db.query(BrokerConnection).filter(
                    BrokerConnection.user_id == user_id,
                    BrokerConnection.is_active == True
                ).first()
            
            if not broker_conn:
                return []
            
            # Get market data for all instruments
            instruments = set()
            for us in user_strategies:
                strategy = db.query(StrategyModel).filter(StrategyModel.id == us.strategy_id).first()
                if strategy and strategy.instrument_filter:
                    # Extract instruments from filter
                    if 'symbols' in strategy.instrument_filter:
                        instruments.update(strategy.instrument_filter['symbols'])
            
            # Fetch market data
            market_data = await self._fetch_market_data(
                broker_conn, list(instruments)
            )
            
            # Generate signals
            signals = []
            for us in user_strategies:
                strategy = db.query(StrategyModel).filter(StrategyModel.id == us.strategy_id).first()
                if not strategy:
                    continue
                
                # Create strategy config
                config = StrategyConfig(
                    id=str(strategy.id),
                    name=strategy.name,
                    category=strategy.category,
                    timeframe=strategy.timeframe,
                    parameters=strategy.parameters or {},
                    entry_rules=strategy.entry_rules or {},
                    exit_rules=strategy.exit_rules or {},
                    target_percent=float(strategy.target_percent),
                    stop_loss_percent=float(strategy.stop_loss_percent),
                    risk_per_trade=float(strategy.risk_per_trade),
                )
                
                # Load strategy
                self.engine.load_strategy(config)
                
                # Get candles for this strategy's instruments
                if config.parameters.get('instrument'):
                    instrument = config.parameters['instrument']
                    if instrument in market_data:
                        candles_df = self._candles_to_dataframe(market_data[instrument].candles)
                        if not candles_df.empty:
                            generated = self.engine.evaluate_strategy(str(strategy.id), candles_df)
                            
                            # Save signals to database
                            for sig in generated:
                                signal_model = SignalModel(
                                    user_id=user_id,
                                    strategy_id=strategy.id,
                                    broker_connection_id=broker_connection_id,
                                    instrument=sig.instrument,
                                    exchange=sig.exchange,
                                    direction=sig.direction,
                                    entry_price=sig.entry_price,
                                    target_price=sig.target_price,
                                    stop_loss_price=sig.stop_loss_price,
                                    risk_reward_ratio=sig.risk_reward_ratio,
                                    expires_at=datetime.utcnow() + timedelta(hours=4),
                                    status='pending',
                                )
                                db.add(signal_model)
                                signals.append(signal_model)
                
                # Unload strategy
                self.engine.unload_strategy(str(strategy.id))
            
            db.commit()
            return signals
            
        finally:
            db.close()
    
    async def _fetch_market_data(
        self,
        broker_conn: BrokerConnection,
        instruments: List[str],
    ) -> Dict[str, MarketData]:
        """Fetch market data from broker."""
        credentials = BrokerCredentials(
            access_token=broker_conn.access_token,
            refresh_token=broker_conn.refresh_token,
            expires_at=broker_conn.expires_at,
        )
        
        adapter = get_broker_adapter(broker_conn.broker_type, credentials)
        
        try:
            market_data = {}
            for instrument in instruments:
                # Get historical candles
                end_date = datetime.utcnow().strftime("%Y-%m-%d")
                start_date = (datetime.utcnow() - timedelta(days=60)).strftime("%Y-%m-%d")
                
                candles = await adapter.get_historical_data(
                    instrument=instrument,
                    exchange="NSE",  # Default
                    interval="15m",
                    from_date=start_date,
                    to_date=end_date,
                )
                
                market_data[instrument] = MarketData(
                    instrument=instrument,
                    exchange="NSE",
                    candles=[{
                        'timestamp': c.timestamp,
                        'open': c.open,
                        'high': c.high,
                        'low': c.low,
                        'close': c.close,
                        'volume': c.volume,
                    } for c in candles]
                )
            
            return market_data
        finally:
            await adapter.close()
    
    def _candles_to_dataframe(self, candles: List[Dict[str, Any]]) -> pd.DataFrame:
        """Convert candles to pandas DataFrame."""
        import pandas as pd
        
        if not candles:
            return pd.DataFrame()
        
        df = pd.DataFrame(candles)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        df.sort_index(inplace=True)
        return df
    
    async def start_auto_generation(
        self,
        user_id: str,
        interval_minutes: int = 15,
    ):
        """Start automatic signal generation for a user."""
        if user_id in self.active_generators:
            return
        
        async def generate_loop():
            while user_id in self.active_generators:
                try:
                    await self.generate_signals_for_user(user_id)
                except Exception as e:
                    print(f"Error generating signals for user {user_id}: {e}")
                
                await asyncio.sleep(interval_minutes * 60)
        
        task = asyncio.create_task(generate_loop())
        self.active_generators[user_id] = task
    
    async def stop_auto_generation(self, user_id: str):
        """Stop automatic signal generation for a user."""
        if user_id in self.active_generators:
            self.active_generators[user_id].cancel()
            try:
                await self.active_generators[user_id]
            except asyncio.CancelledError:
                pass
            del self.active_generators[user_id]
    
    async def get_pending_signals(
        self,
        user_id: str,
        strategy_id: Optional[str] = None,
    ) -> List[SignalModel]:
        """Get pending signals for a user."""
        db = next(get_db())
        
        try:
            query = db.query(SignalModel).filter(
                SignalModel.user_id == user_id,
                SignalModel.status == 'pending',
            )
            
            if strategy_id:
                query = query.filter(SignalModel.strategy_id == strategy_id)
            
            return query.order_by(SignalModel.detected_at.desc()).all()
        finally:
            db.close()
    
    async def execute_signal(
        self,
        signal_id: str,
        user_id: str,
        broker_connection_id: str,
        quantity: Optional[float] = None,
    ) -> Optional[SignalModel]:
        """Execute a signal by placing an order."""
        db = next(get_db())
        
        try:
            signal = db.query(SignalModel).filter(
                SignalModel.id == signal_id,
                SignalModel.user_id == user_id,
                SignalModel.status == 'pending',
            ).first()
            
            if not signal:
                return None
            
            # Get broker connection
            broker_conn = db.query(BrokerConnection).filter(
                BrokerConnection.id == broker_connection_id,
                BrokerConnection.user_id == user_id,
            ).first()
            
            if not broker_conn:
                return None
            
            # Place order via broker
            credentials = BrokerCredentials(
                access_token=broker_conn.access_token,
                refresh_token=broker_conn.refresh_token,
                expires_at=broker_conn.expires_at,
            )
            
            adapter = get_broker_adapter(broker_conn.broker_type, credentials)
            
            try:
                order_params = {
                    'exchange': signal.exchange,
                    'instrument': signal.instrument,
                    'transaction_type': 'BUY' if signal.direction == 'LONG' else 'SELL',
                    'order_type': 'MARKET',
                    'product': 'MIS',
                    'quantity': quantity or 1,
                    'price': signal.entry_price,
                }
                
                order_result = await adapter.place_order(order_params)
                
                # Update signal
                signal.status = 'executed'
                signal.order_id = order_result.broker_order_id
                signal.filled_quantity = order_result.filled_quantity
                signal.entry_price = order_result.average_price or order_result.price
                
                db.commit()
                return signal
                
            finally:
                await adapter.close()
                
        finally:
            db.close()
    
    async def invalidate_signal(self, signal_id: str, user_id: str) -> bool:
        """Mark a signal as invalidated."""
        db = next(get_db())
        
        try:
            signal = db.query(SignalModel).filter(
                SignalModel.id == signal_id,
                SignalModel.user_id == user_id,
                SignalModel.status == 'pending',
            ).first()
            
            if not signal:
                return False
            
            signal.status = 'invalidated'
            db.commit()
            return True
        finally:
            db.close()
    
    async def cleanup_expired_signals(self) -> int:
        """Clean up expired signals."""
        db = next(get_db())
        
        try:
            expired = db.query(SignalModel).filter(
                SignalModel.status == 'pending',
                SignalModel.expires_at < datetime.utcnow(),
            ).all()
            
            for signal in expired:
                signal.status = 'expired'
            
            db.commit()
            return len(expired)
        finally:
            db.close()


# Global signal generator instance
signal_generator = SignalGenerator()