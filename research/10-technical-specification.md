# AlgoReady Research - Technical Specification

**Date**: 2026-11-24
**Investigator**: OpenCode AI Agent
**Purpose**: Technical architecture and implementation plan for AlgoReady platform

---

## HIGH-LEVEL ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────┐
│                    ALGOREADY PLATFORM                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐      │
│  │   Web App   │     │ Chrome Extn │     │   Backend   │      │
│  │  (Next.js)  │◄───►│ (MV3 Ext)   │◄───►│  (Python)   │      │
│  └─────────────┘     └─────────────┘     └─────────────┘      │
│         │                    │                   │            │
│         ▼                    ▼                   ▼            │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐      │
│  │  Database   │     │  Browser    │     │   Market    │      │
│  │   (Postgr)  │     │   Storage   │     │    Data     │      │
│  └─────────────┘     └─────────────┘     └─────────────┘      │
│         │                                       │            │
│         ▼                                       ▼            │
│  ┌─────────────┐                         ┌─────────────┐     │
│  │   Cache     │                         │  Brokers    │     │
│  │    (Redis)  │◄───────────────────────►│  APIs (Z/U/F)│     │
│  └─────────────┘                         └─────────────┘     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## TECHNOLOGY STACK

### Frontend (Web Application)
| Layer | Technology | Reason |
|-------|------------|--------|
| Framework | Next.js 15 (App Router) | SSR, SEO, Performance |
| Language | TypeScript | Type safety |
| Styling | Tailwind CSS | Rapid UI development |
| Charts | TradingView Lightweight Charts | Financial charting |
| State Mgmt | React Context + Zustand | Simple, performant |
| HTTP Client | Fetch API / Axios | Standard |
| Build | TurboPack / Webpack | Fast builds |

### Chrome Extension
| Component | Technology | Reason |
|-----------|------------|--------|
| Manifest | V3 | Standard, future-proof |
| Framework | React + TypeScript | Same as web |
| State Mgmt | React Context | Simple |
| Storage | Chrome Storage API | Built-in |
| Background | Service Worker | MV3 requirement |
| Overlay | Shadow DOM | Isolation |

### Backend API
| Layer | Technology | Reason |
|-------|------------|--------|
| Framework | FastAPI (Python 3.12) | Async, typed, auto-docs |
| Language | Python 3.12 | Ecosystem |
| Database | PostgreSQL 16 | Reliability, extensions |
| Cache | Redis 7 | Sessions, market data |
| WebSocket | WebSocket (uvicorn) | Real-time data |
| Authentication | JWT + OAuth2 | Standard |
| Rate Limiting | Redis-based | Configurable |

### Infrastructure
| Component | Technology | Reason |
|-----------|------------|--------|
| Deployment | Cloudflare Pages | Edge, free tier |
| API Routes | Cloudflare Workers | Serverless |
| Database | Supabase | Managed Postgres |
| Cache | Upstash | Serverless Redis |
| DNS | Cloudflare | CDN, security |

---

## DATABASE SCHEMA

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    phone VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE
);
```

### Broker Connections Table
```sql
CREATE TABLE broker_connections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    broker_type VARCHAR(50) NOT NULL, -- 'zerodha', 'upstox', 'fyers'
    account_id VARCHAR(255) NOT NULL, -- Broker's account ID
    access_token TEXT NOT NULL, -- Encrypted
    refresh_token TEXT, -- Nullable, encrypted
    expires_at TIMESTAMP WITH TIME ZONE,
    connected_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_synced TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE,
    UNIQUE(user_id, broker_type, account_id)
);
```

### Strategies Table
```sql
CREATE TABLE strategies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100), -- 'scalping', 'momentum', etc.
    market VARCHAR(50), -- 'india_stocks', 'crypto', 'us_stocks'
    instrument_filter JSONB, -- Pattern for instruments
    timeframe VARCHAR(20), -- '1m', '5m', '15m', '1h', '1d'
    parameters JSONB, -- Strategy parameters
    entry_rules JSONB, -- Entry rule definitions
    exit_rules JSONB, -- Exit rule definitions
    target_percent DECIMAL(10, 2),
    stop_loss_percent DECIMAL(10, 2),
    risk_per_trade DECIMAL(10, 2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE,
    is_public BOOLEAN DEFAULT FALSE
);
```

### User Strategies Table
```sql
CREATE TABLE user_strategies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    strategy_id UUID REFERENCES strategies(id) ON DELETE CASCADE,
    broker_connection_id UUID REFERENCES broker_connections(id),
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE,
    configuration JSONB, -- User-specific parameters
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Signals Table
```sql
CREATE TABLE signals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    strategy_id UUID REFERENCES strategies(id),
    broker_connection_id UUID REFERENCES broker_connections(id),
    instrument VARCHAR(255) NOT NULL,
    exchange VARCHAR(50) NOT NULL,
    direction VARCHAR(10) NOT NULL, -- 'LONG' or 'SHORT'
    entry_price DECIMAL(20, 5),
    target_price DECIMAL(20, 5),
    stop_loss_price DECIMAL(20, 5),
    risk_reward_ratio DECIMAL(10, 2),
    detected_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE,
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'executed', 'invalidated', 'expired'
    order_id VARCHAR(255), -- When executed
    filled_quantity DECIMAL(20, 5),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Positions Table
```sql
CREATE TABLE positions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    broker_connection_id UUID REFERENCES broker_connections(id),
    instrument VARCHAR(255) NOT NULL,
    exchange VARCHAR(50) NOT NULL,
    direction VARCHAR(10) NOT NULL,
    quantity DECIMAL(20, 5) NOT NULL,
    avg_entry_price DECIMAL(20, 5) NOT NULL,
    current_price DECIMAL(20, 5),
    unrealized_pnl DECIMAL(20, 5),
    realized_pnl DECIMAL(20, 5) DEFAULT 0,
    product_type VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, broker_connection_id, instrument, direction)
);
```

### Orders Table
```sql
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    broker_connection_id UUID REFERENCES broker_connections(id),
    signal_id UUID REFERENCES signals(id),
    exchange VARCHAR(50) NOT NULL,
    instrument VARCHAR(255) NOT NULL,
    transaction_type VARCHAR(10) NOT NULL, -- 'BUY', 'SELL'
    order_type VARCHAR(20), -- 'MARKET', 'LIMIT'
    product VARCHAR(10), -- 'MIS', 'CNC', etc.
    quantity DECIMAL(20, 5) NOT NULL,
    price DECIMAL(20, 5),
    trigger_price DECIMAL(20, 5),
    order_status VARCHAR(50), -- 'PENDING', 'OPEN', 'CANCELLED', 'COMPLETE', 'REJECTED'
    broker_order_id VARCHAR(255),
    placed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Subscriptions Table
```sql
CREATE TABLE subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    plan_type VARCHAR(50) NOT NULL, -- 'free', 'pro', 'premium'
    payment_id VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active',
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## API ENDPOINTS (FastAPI)

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/logout` - User logout
- `GET /api/v1/auth/profile` - Get user profile

### Broker Integration
- `GET /api/v1/brokers` - List supported brokers
- `POST /api/v1/brokers/{broker}/connect` - Initiate broker connection
- `GET /api/v1/brokers/{broker}/callback` - OAuth callback
- `GET /api/v1/brokers` - List user brokers
- `GET /api/v1/brokers/{id}` - Get broker status
- `DELETE /api/v1/brokers/{id}` - Disconnect broker

### Strategies
- `GET /api/v1/strategies` - List strategies
- `GET /api/v1/strategies/{id}` - Get strategy details
- `POST /api/v1/strategies` - Create strategy (admin)
- `POST /api/v1/strategies/{id}/apply` - Apply to chart
- `DELETE /api/v1/user-strategies/{id}` - Remove applied strategy

### Signals
- `GET /api/v1/signals` - List signals
- `GET /api/v1/signals/active` - Get active signals
- `POST /api/v1/signals/{id}/execute` - Execute signal
- `PATCH /api/v1/signals/{id}` - Update signal status

### Positions
- `GET /api/v1/positions` - List positions
- `GET /api/v1/positions/{instrument}` - Get position

### Orders
- `GET /api/v1/orders` - List orders
- `POST /api/v1/orders` - Place order
- `PUT /api/v1/orders/{id}` - Modify order
- `DELETE /api/v1/orders/{id}` - Cancel order

### Market Data
- `GET /api/v1/market/quotes` - Get multiple quotes
- `GET /api/v1/market/quotes/{instrument}` - Get single quote
- `GET /api/v1/market/history` - Historical data
- `GET /api/v1/market/instruments` - Instrument search

### Backtesting
- `POST /api/v1/backtest` - Run backtest
- `GET /api/v1/backtest/{id}` - Get results

### Subscription
- `GET /api/v1/subscription` - Get user subscription
- `POST /api/v1/subscription/checkout` - Create checkout
- `POST /api/v1/subscription/webhook` - Payment webhook

---

## CHROME EXTENSION ARCHITECTURE

### Manifest V3 Structure
```json
{
  "manifest_version": 3,
  "name": "AlgoReady Trading Extension",
  "version": "1.0.0",
  "permissions": [
    "activeTab",
    "storage",
    "notifications",
    "alarms"
  ],
  "host_permissions": [
    "https://api.algoready.dev/*",
    "https://*.zing.trade/*"
  ],
  "background": {
    "service_worker": "background.js"
  },
  "action": {
    "default_popup": "popup.html",
    "default_icon": "icons/icon-16.png"
  },
  "side_panel": {
    "default_path": "sidepanel.html"
  },
  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["content.js"],
      "run_at": "document_end"
    }
  ]
}
```

### Content Script Flow
1. Detect broker website
2. Identify active chart
3. Detect instrument/exchange/timeframe
4. Inject overlay at appropriate location
5. Listen for user interactions
6. Communicate with background script

---

## STRATEGY ENGINE DESIGN

### Strategy Interface
```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel

class Strategy(ABC):
    @abstractmethod
    async def analyze(self, candles: list, parameters: Dict[str, Any]) -> Optional[dict]:
        """Analyze market data and return signal if conditions met"""
        pass
    
    @abstractmethod
    async def validate(self, instrument: str, timeframe: str) -> bool:
        """Check if strategy can be applied to instrument/timeframe"""
        pass
```

### Example Strategy Implementation
```python
class EMACrossStrategy(Strategy):
    def __init__(self, fast_period: int = 9, slow_period: int = 21):
        self.fast_period = fast_period
        self.slow_period = slow_period
    
    async def analyze(self, candles: list, parameters: Dict[str, Any]) -> Optional[dict]:
        # Calculate EMAs
        # Check crossover conditions
        # Return signal dict if conditions met
        pass
```

### Indicators Library
- EMA (Exponential Moving Average)
- SMA (Simple Moving Average)
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Bollinger Bands
- ATR (Average True Range)
- VWAP (Volume Weighted Average Price)
- Supertrend

---

## SECURITY CONSIDERATIONS

### Token Storage
- Never store in localStorage
- Encrypt at rest in database
- Use HttpOnly Secure cookies
- Implement token rotation

### OAuth Security
- Validate state parameter
- Use PKCE for additional security
- Limit redirect URIs
- Monitor for suspicious activity

### Data Validation
- Input sanitization on all endpoints
- SQL injection prevention (ORM/prepared statements)
- Rate limiting per user/IP
- CORS policy restrictions

### WebSocket Security
- Token-based authentication
- Origin validation
- Message rate limiting
- Connection timeout handling

---

## DEPLOYMENT ARCHITECTURE

### Cloudflare Pages (Frontend)
- Build command: `npm run build`
- Output directory: `.next`
- Environment variables via Pages dashboard
- Custom domain: algoready.pages.dev

### Cloudflare Workers (API)
- Deploy via Wrangler
- Connect to PostgreSQL via connection pooling
- Redis via Upstash for caching
- WebSocket via durable objects

### Database
- Supabase (PostgreSQL 16)
- Connection pooling
- SSL required
- Automated backups

---

## MONITORING & LOGGING

### Error Tracking
- Sentry for frontend errors
- Sentry for backend errors
- Custom error logging for critical events

### Performance Monitoring
- Cloudflare analytics
- Response time tracking
- Database query performance
- WebSocket connection health

---

## NOTES

1. Python FastAPI chosen for async performance
2. PostgreSQL for reliability and GIS extensions
3. Redis for session caching and rate limiting
4. TradingView Lightweight Charts for financial visualization
5. Next.js App Router for modern React patterns

---

## PHASE 1 IMPLEMENTATION PRIORITIES

1. **Database Schema** - Create all tables
2. **Authentication System** - Register/Login with JWT
3. **Broker Integration (Zerodha)** - OAuth flow, API wrappers
4. **Strategy Engine** - Core framework with sample strategies
5. **Web UI** - Dashboard and basic components
6. **API Layer** - All backend endpoints

---

**Last Updated**: 2026-11-24