"""Strategy engine for evaluating strategies and generating signals."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
import json
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod


@dataclass
class StrategyConfig:
    """Strategy configuration."""
    id: str
    name: str
    category: str
    timeframe: str
    parameters: Dict[str, Any]
    entry_rules: Dict[str, Any]
    exit_rules: Dict[str, Any]
    target_percent: float
    stop_loss_percent: float
    risk_per_trade: float


@dataclass
class Signal:
    """Generated signal."""
    instrument: str
    exchange: str
    direction: str  # LONG or SHORT
    entry_price: float
    target_price: float
    stop_loss_price: float
    risk_reward_ratio: float
    confidence: float
    metadata: Dict[str, Any]


class BaseStrategy(ABC):
    """Base class for all strategies."""
    
    def __init__(self, config: StrategyConfig):
        self.config = config
    
    @abstractmethod
    def evaluate(self, candles: pd.DataFrame) -> List[Signal]:
        """Evaluate strategy on candle data."""
        pass
    
    def _calculate_indicators(self, candles: pd.DataFrame) -> pd.DataFrame:
        """Calculate common indicators."""
        df = candles.copy()
        
        # Moving averages
        df['sma_20'] = df['close'].rolling(20).mean()
        df['sma_50'] = df['close'].rolling(50).mean()
        df['ema_9'] = df['close'].ewm(span=9).mean()
        df['ema_21'] = df['close'].ewm(span=21).mean()
        
        # RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # MACD
        ema_12 = df['close'].ewm(span=12).mean()
        ema_26 = df['close'].ewm(span=26).mean()
        df['macd'] = ema_12 - ema_26
        df['macd_signal'] = df['macd'].ewm(span=9).mean()
        df['macd_hist'] = df['macd'] - df['macd_signal']
        
        # Bollinger Bands
        df['bb_middle'] = df['close'].rolling(20).mean()
        bb_std = df['close'].rolling(20).std()
        df['bb_upper'] = df['bb_middle'] + (bb_std * 2)
        df['bb_lower'] = df['bb_middle'] - (bb_std * 2)
        
        # ATR
        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df['close'].shift())
        low_close = np.abs(df['low'] - df['close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = ranges.max(axis=1)
        df['atr'] = true_range.rolling(14).mean()
        
        # Volume indicators
        df['volume_sma'] = df['volume'].rolling(20).mean()
        df['volume_ratio'] = df['volume'] / df['volume_sma']
        
        return df


class MomentumStrategy(BaseStrategy):
    """Momentum-based strategy."""
    
    def evaluate(self, candles: pd.DataFrame) -> List[Signal]:
        df = self._calculate_indicators(candles)
        signals = []
        
        if len(df) < 50:
            return signals
        
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        # Parameters
        rsi_oversold = self.config.parameters.get('rsi_oversold', 30)
        rsi_overbought = self.config.parameters.get('rsi_overbought', 70)
        volume_threshold = self.config.parameters.get('volume_threshold', 1.5)
        
        # Long condition: RSI oversold + MACD crossover + volume spike
        if (prev['rsi'] < rsi_oversold and latest['rsi'] > rsi_oversold and
            prev['macd'] < prev['macd_signal'] and latest['macd'] > latest['macd_signal'] and
            latest['volume_ratio'] > volume_threshold):
            
            entry = latest['close']
            stop_loss = entry * (1 - self.config.stop_loss_percent / 100)
            target = entry * (1 + self.config.target_percent / 100)
            
            signals.append(Signal(
                instrument=self.config.parameters.get('instrument', ''),
                exchange=self.config.parameters.get('exchange', 'NSE'),
                direction='LONG',
                entry_price=entry,
                target_price=target,
                stop_loss_price=stop_loss,
                risk_reward_ratio=self.config.target_percent / self.config.stop_loss_percent,
                confidence=0.75,
                metadata={
                    'rsi': latest['rsi'],
                    'macd': latest['macd'],
                    'volume_ratio': latest['volume_ratio'],
                }
            ))
        
        # Short condition: RSI overbought + MACD crossunder + volume spike
        if (prev['rsi'] > rsi_overbought and latest['rsi'] < rsi_overbought and
            prev['macd'] > prev['macd_signal'] and latest['macd'] < latest['macd_signal'] and
            latest['volume_ratio'] > volume_threshold):
            
            entry = latest['close']
            stop_loss = entry * (1 + self.config.stop_loss_percent / 100)
            target = entry * (1 - self.config.target_percent / 100)
            
            signals.append(Signal(
                instrument=self.config.parameters.get('instrument', ''),
                exchange=self.config.parameters.get('exchange', 'NSE'),
                direction='SHORT',
                entry_price=entry,
                target_price=target,
                stop_loss_price=stop_loss,
                risk_reward_ratio=self.config.target_percent / self.config.stop_loss_percent,
                confidence=0.75,
                metadata={
                    'rsi': latest['rsi'],
                    'macd': latest['macd'],
                    'volume_ratio': latest['volume_ratio'],
                }
            ))
        
        return signals


class BreakoutStrategy(BaseStrategy):
    """Breakout strategy using Bollinger Bands and volume."""
    
    def evaluate(self, candles: pd.DataFrame) -> List[Signal]:
        df = self._calculate_indicators(candles)
        signals = []
        
        if len(df) < 20:
            return signals
        
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        # Parameters
        bb_period = self.config.parameters.get('bb_period', 20)
        volume_multiplier = self.config.parameters.get('volume_multiplier', 2.0)
        
        # Long breakout: Price breaks above upper BB with volume
        if (prev['close'] <= prev['bb_upper'] and latest['close'] > latest['bb_upper'] and
            latest['volume_ratio'] > volume_multiplier):
            
            entry = latest['close']
            stop_loss = latest['bb_middle']  # Middle band as stop
            target = entry * (1 + self.config.target_percent / 100)
            
            signals.append(Signal(
                instrument=self.config.parameters.get('instrument', ''),
                exchange=self.config.parameters.get('exchange', 'NSE'),
                direction='LONG',
                entry_price=entry,
                target_price=target,
                stop_loss_price=stop_loss,
                risk_reward_ratio=self.config.target_percent / self.config.stop_loss_percent,
                confidence=0.7,
                metadata={
                    'bb_upper': latest['bb_upper'],
                    'bb_middle': latest['bb_middle'],
                    'volume_ratio': latest['volume_ratio'],
                }
            ))
        
        # Short breakout: Price breaks below lower BB with volume
        if (prev['close'] >= prev['bb_lower'] and latest['close'] < latest['bb_lower'] and
            latest['volume_ratio'] > volume_multiplier):
            
            entry = latest['close']
            stop_loss = latest['bb_middle']
            target = entry * (1 - self.config.target_percent / 100)
            
            signals.append(Signal(
                instrument=self.config.parameters.get('instrument', ''),
                exchange=self.config.parameters.get('exchange', 'NSE'),
                direction='SHORT',
                entry_price=entry,
                target_price=target,
                stop_loss_price=stop_loss,
                risk_reward_ratio=self.config.target_percent / self.config.stop_loss_percent,
                confidence=0.7,
                metadata={
                    'bb_lower': latest['bb_lower'],
                    'bb_middle': latest['bb_middle'],
                    'volume_ratio': latest['volume_ratio'],
                }
            ))
        
        return signals


class ReversionStrategy(BaseStrategy):
    """Mean reversion strategy."""
    
    def evaluate(self, candles: pd.DataFrame) -> List[Signal]:
        df = self._calculate_indicators(candles)
        signals = []
        
        if len(df) < 20:
            return signals
        
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        # Parameters
        rsi_oversold = self.config.parameters.get('rsi_oversold', 25)
        rsi_overbought = self.config.parameters.get('rsi_overbought', 75)
        bb_threshold = self.config.parameters.get('bb_threshold', 0.02)  # 2% from band
        
        # Long reversion: Price near lower BB, RSI oversold
        bb_position = (latest['close'] - latest['bb_lower']) / (latest['bb_upper'] - latest['bb_lower'])
        
        if bb_position < bb_threshold and latest['rsi'] < rsi_oversold:
            entry = latest['close']
            stop_loss = entry * (1 - self.config.stop_loss_percent / 100)
            target = latest['bb_middle']  # Target middle band
            
            signals.append(Signal(
                instrument=self.config.parameters.get('instrument', ''),
                exchange=self.config.parameters.get('exchange', 'NSE'),
                direction='LONG',
                entry_price=entry,
                target_price=target,
                stop_loss_price=stop_loss,
                risk_reward_ratio=abs(target - entry) / abs(entry - stop_loss),
                confidence=0.65,
                metadata={
                    'bb_position': bb_position,
                    'rsi': latest['rsi'],
                }
            ))
        
        # Short reversion: Price near upper BB, RSI overbought
        if bb_position > (1 - bb_threshold) and latest['rsi'] > rsi_overbought:
            entry = latest['close']
            stop_loss = entry * (1 + self.config.stop_loss_percent / 100)
            target = latest['bb_middle']
            
            signals.append(Signal(
                instrument=self.config.parameters.get('instrument', ''),
                exchange=self.config.parameters.get('exchange', 'NSE'),
                direction='SHORT',
                entry_price=entry,
                target_price=target,
                stop_loss_price=stop_loss,
                risk_reward_ratio=abs(entry - target) / abs(stop_loss - entry),
                confidence=0.65,
                metadata={
                    'bb_position': bb_position,
                    'rsi': latest['rsi'],
                }
            ))
        
        return signals


class ScalpingStrategy(BaseStrategy):
    """Scalping strategy using EMA crossovers."""
    
    def evaluate(self, candles: pd.DataFrame) -> List[Signal]:
        df = self._calculate_indicators(candles)
        signals = []
        
        if len(df) < 21:
            return signals
        
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        # Parameters
        fast_ema = self.config.parameters.get('fast_ema', 9)
        slow_ema = self.config.parameters.get('slow_ema', 21)
        
        # Long: Fast EMA crosses above slow EMA
        if prev[f'ema_{fast_ema}'] < prev[f'ema_{slow_ema}'] and latest[f'ema_{fast_ema}'] > latest[f'ema_{slow_ema}']:
            entry = latest['close']
            stop_loss = entry * (1 - self.config.stop_loss_percent / 100)
            target = entry * (1 + self.config.target_percent / 100)
            
            signals.append(Signal(
                instrument=self.config.parameters.get('instrument', ''),
                exchange=self.config.parameters.get('exchange', 'NSE'),
                direction='LONG',
                entry_price=entry,
                target_price=target,
                stop_loss_price=stop_loss,
                risk_reward_ratio=self.config.target_percent / self.config.stop_loss_percent,
                confidence=0.6,
                metadata={
                    f'ema_{fast_ema}': latest[f'ema_{fast_ema}'],
                    f'ema_{slow_ema}': latest[f'ema_{slow_ema}'],
                }
            ))
        
        # Short: Fast EMA crosses below slow EMA
        if prev[f'ema_{fast_ema}'] > prev[f'ema_{slow_ema}'] and latest[f'ema_{fast_ema}'] < latest[f'ema_{slow_ema}']:
            entry = latest['close']
            stop_loss = entry * (1 + self.config.stop_loss_percent / 100)
            target = entry * (1 - self.config.target_percent / 100)
            
            signals.append(Signal(
                instrument=self.config.parameters.get('instrument', ''),
                exchange=self.config.parameters.get('exchange', 'NSE'),
                direction='SHORT',
                entry_price=entry,
                target_price=target,
                stop_loss_price=stop_loss,
                risk_reward_ratio=self.config.target_percent / self.config.stop_loss_percent,
                confidence=0.6,
                metadata={
                    f'ema_{fast_ema}': latest[f'ema_{fast_ema}'],
                    f'ema_{slow_ema}': latest[f'ema_{slow_ema}'],
                }
            ))
        
        return signals


class OptionsStrategy(BaseStrategy):
    """Options strategy base."""
    
    def evaluate(self, candles: pd.DataFrame) -> List[Signal]:
        # Options strategies require option chain data
        # This is a placeholder for future implementation
        return []


class CustomStrategy(BaseStrategy):
    """Custom strategy with user-defined rules."""
    
    def evaluate(self, candles: pd.DataFrame) -> List[Signal]:
        df = self._calculate_indicators(candles)
        signals = []
        
        if len(df) < 50:
            return signals
        
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        # Evaluate custom entry rules
        entry_rules = self.config.entry_rules
        exit_rules = self.config.exit_rules
        
        # Simple rule evaluation (would be more complex in production)
        long_condition = True
        short_condition = True
        
        # Check entry conditions
        if 'rsi_below' in entry_rules:
            long_condition &= latest['rsi'] < entry_rules['rsi_below']
        if 'rsi_above' in entry_rules:
            short_condition &= latest['rsi'] > entry_rules['rsi_above']
        if 'macd_crossover' in entry_rules and entry_rules['macd_crossover']:
            long_condition &= prev['macd'] < prev['macd_signal'] and latest['macd'] > latest['macd_signal']
            short_condition &= prev['macd'] > prev['macd_signal'] and latest['macd'] < latest['macd_signal']
        if 'price_above_sma' in entry_rules:
            long_condition &= latest['close'] > latest[f"sma_{entry_rules['price_above_sma']}"]
        if 'price_below_sma' in entry_rules:
            short_condition &= latest['close'] < latest[f"sma_{entry_rules['price_below_sma']}"]
        
        if long_condition:
            entry = latest['close']
            stop_loss = entry * (1 - self.config.stop_loss_percent / 100)
            target = entry * (1 + self.config.target_percent / 100)
            
            signals.append(Signal(
                instrument=self.config.parameters.get('instrument', ''),
                exchange=self.config.parameters.get('exchange', 'NSE'),
                direction='LONG',
                entry_price=entry,
                target_price=target,
                stop_loss_price=stop_loss,
                risk_reward_ratio=self.config.target_percent / self.config.stop_loss_percent,
                confidence=0.7,
                metadata={'custom': True}
            ))
        
        if short_condition:
            entry = latest['close']
            stop_loss = entry * (1 + self.config.stop_loss_percent / 100)
            target = entry * (1 - self.config.target_percent / 100)
            
            signals.append(Signal(
                instrument=self.config.parameters.get('instrument', ''),
                exchange=self.config.parameters.get('exchange', 'NSE'),
                direction='SHORT',
                entry_price=entry,
                target_price=target,
                stop_loss_price=stop_loss,
                risk_reward_ratio=self.config.target_percent / self.config.stop_loss_percent,
                confidence=0.7,
                metadata={'custom': True}
            ))
        
        return signals


class StrategyEngine:
    """Main strategy engine for running strategies."""
    
    def __init__(self):
        self.strategies: Dict[str, BaseStrategy] = {}
        self.strategy_classes = {
            'momentum': MomentumStrategy,
            'breakout': BreakoutStrategy,
            'reversion': ReversionStrategy,
            'scalping': ScalpingStrategy,
            'options': OptionsStrategy,
            'custom': CustomStrategy,
        }
    
    def load_strategy(self, config: StrategyConfig) -> BaseStrategy:
        """Load a strategy from config."""
        strategy_class = self.strategy_classes.get(config.category)
        if not strategy_class:
            raise ValueError(f"Unknown strategy category: {config.category}")
        
        strategy = strategy_class(config)
        self.strategies[config.id] = strategy
        return strategy
    
    def unload_strategy(self, strategy_id: str):
        """Unload a strategy."""
        if strategy_id in self.strategies:
            del self.strategies[strategy_id]
    
    def evaluate_strategy(self, strategy_id: str, candles: pd.DataFrame) -> List[Signal]:
        """Evaluate a specific strategy."""
        if strategy_id not in self.strategies:
            raise ValueError(f"Strategy not loaded: {strategy_id}")
        
        return self.strategies[strategy_id].evaluate(candles)
    
    def evaluate_all(self, candles_dict: Dict[str, pd.DataFrame]) -> Dict[str, List[Signal]]:
        """Evaluate all loaded strategies."""
        results = {}
        for strategy_id, strategy in self.strategies.items():
            instrument = strategy.config.parameters.get('instrument')
            if instrument in candles_dict:
                results[strategy_id] = strategy.evaluate(candles_dict[instrument])
            else:
                results[strategy_id] = []
        return results
    
    def backtest(
        self,
        strategy_config: StrategyConfig,
        candles: pd.DataFrame,
        initial_capital: float = 100000,
        commission: float = 0.0003,
        slippage: float = 0.0001,
    ) -> Dict[str, Any]:
        """Run backtest on a strategy."""
        strategy = self.strategy_classes[strategy_config.category](strategy_config)
        signals = strategy.evaluate(candles)
        
        # Simulate trades
        capital = initial_capital
        position = None
        trades = []
        equity_curve = [{'timestamp': candles.index[0], 'equity': capital}]
        
        for i, row in candles.iterrows():
            # Check for signals at this timestamp
            for signal in signals:
                if signal.entry_price <= row['high'] and signal.entry_price >= row['low']:
                    # Enter trade
                    if position is None:
                        qty = (capital * strategy_config.risk_per_trade / 100) / (signal.entry_price - signal.stop_loss_price)
                        qty = max(1, int(qty))
                        
                        cost = qty * signal.entry_price * (1 + commission + slippage)
                        if cost <= capital:
                            position = {
                                'direction': signal.direction,
                                'entry_price': signal.entry_price,
                                'target': signal.target_price,
                                'stop_loss': signal.stop_loss_price,
                                'quantity': qty,
                                'entry_time': i,
                            }
                            capital -= cost
            
            # Check exit conditions
            if position:
                if position['direction'] == 'LONG':
                    if row['low'] <= position['stop_loss']:
                        # Stop loss hit
                        pnl = (position['stop_loss'] - position['entry_price']) * position['quantity']
                        capital += position['quantity'] * position['stop_loss'] * (1 - commission - slippage)
                        trades.append({
                            'entry_time': position['entry_time'],
                            'exit_time': i,
                            'direction': 'LONG',
                            'entry_price': position['entry_price'],
                            'exit_price': position['stop_loss'],
                            'quantity': position['quantity'],
                            'pnl': pnl,
                            'exit_reason': 'SL',
                        })
                        position = None
                    elif row['high'] >= position['target']:
                        # Target hit
                        pnl = (position['target'] - position['entry_price']) * position['quantity']
                        capital += position['quantity'] * position['target'] * (1 - commission - slippage)
                        trades.append({
                            'entry_time': position['entry_time'],
                            'exit_time': i,
                            'direction': 'LONG',
                            'entry_price': position['entry_price'],
                            'exit_price': position['target'],
                            'quantity': position['quantity'],
                            'pnl': pnl,
                            'exit_reason': 'TARGET',
                        })
                        position = None
                else:  # SHORT
                    if row['high'] >= position['stop_loss']:
                        pnl = (position['entry_price'] - position['stop_loss']) * position['quantity']
                        capital += position['quantity'] * (2 * position['entry_price'] - position['stop_loss']) * (1 - commission - slippage)
                        trades.append({
                            'entry_time': position['entry_time'],
                            'exit_time': i,
                            'direction': 'SHORT',
                            'entry_price': position['entry_price'],
                            'exit_price': position['stop_loss'],
                            'quantity': position['quantity'],
                            'pnl': pnl,
                            'exit_reason': 'SL',
                        })
                        position = None
                    elif row['low'] <= position['target']:
                        pnl = (position['entry_price'] - position['target']) * position['quantity']
                        capital += position['quantity'] * (2 * position['entry_price'] - position['target']) * (1 - commission - slippage)
                        trades.append({
                            'entry_time': position['entry_time'],
                            'exit_time': i,
                            'direction': 'SHORT',
                            'entry_price': position['entry_price'],
                            'exit_price': position['target'],
                            'quantity': position['quantity'],
                            'pnl': pnl,
                            'exit_reason': 'TARGET',
                        })
                        position = None
            
            equity_curve.append({'timestamp': i, 'equity': capital})
        
        # Close any open position at end
        if position:
            last_price = candles.iloc[-1]['close']
            if position['direction'] == 'LONG':
                pnl = (last_price - position['entry_price']) * position['quantity']
            else:
                pnl = (position['entry_price'] - last_price) * position['quantity']
            
            capital += position['quantity'] * last_price * (1 - commission - slippage)
            trades.append({
                'entry_time': position['entry_time'],
                'exit_time': candles.index[-1],
                'direction': position['direction'],
                'entry_price': position['entry_price'],
                'exit_price': last_price,
                'quantity': position['quantity'],
                'pnl': pnl,
                'exit_reason': 'EOD',
            })
        
        # Calculate metrics
        if trades:
            winning = [t for t in trades if t['pnl'] > 0]
            losing = [t for t in trades if t['pnl'] <= 0]
            
            total_pnl = sum(t['pnl'] for t in trades)
            win_rate = len(winning) / len(trades) * 100
            avg_win = sum(t['pnl'] for t in winning) / len(winning) if winning else 0
            avg_loss = sum(t['pnl'] for t in losing) / len(losing) if losing else 0
            max_win = max(t['pnl'] for t in trades)
            max_loss = min(t['pnl'] for t in trades)
            profit_factor = abs(sum(t['pnl'] for t in winning) / sum(t['pnl'] for t in losing)) if losing else float('inf')
            
            returns = pd.Series([t['pnl'] for t in trades])
            sharpe = returns.mean() / returns.std() * np.sqrt(252) if returns.std() > 0 else 0
            
            # Max drawdown
            equity_series = pd.Series([e['equity'] for e in equity_curve])
            rolling_max = equity_series.expanding().max()
            drawdown = (equity_series - rolling_max) / rolling_max * 100
            max_drawdown = drawdown.min()
        else:
            total_pnl = 0
            win_rate = 0
            avg_win = 0
            avg_loss = 0
            max_win = 0
            max_loss = 0
            profit_factor = 0
            sharpe = 0
            max_drawdown = 0
        
        return {
            'total_trades': len(trades),
            'winning_trades': len(winning) if trades else 0,
            'losing_trades': len(losing) if trades else 0,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe,
            'sortino_ratio': 0,  # Placeholder
            'profit_factor': profit_factor,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'max_win': max_win,
            'max_loss': max_loss,
            'trades': trades,
            'equity_curve': equity_curve,
        }


# Global engine instance
engine = StrategyEngine()