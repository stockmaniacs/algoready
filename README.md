# AlgoReady

**Your Brokers. Your Strategies. One Trading Workspace.**

A powerful, open-source trading platform built for modern traders. Connect your broker accounts, apply pre-built trading strategies, and execute trades directly on your charts.

## 🌟 Features

- **Multi-Broker Support**: Connect Zerodha (Kite), Upstox, and FYERS accounts
- **Strategy Marketplace**: Apply expert-curated trading strategies
- **Real-time Signals**: Get structured trade setups with entry, target, and stop-loss
- **Chart Overlays**: Visual markers directly on your trading charts
- **Position Tracking**: Real-time position monitoring across accounts
- **Order Management**: Full order placement and management
- **Backtesting**: Test strategies on historical data
- **Chrome Extension**: Seamless integration with broker platforms

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ or Python 3.10+
- PostgreSQL database
- Redis (optional, for caching)
- Valid broker account

### Installation

```bash
# Clone the repository
git clone https://github.com/stockmaniacs/algoready.git
cd algoready

# Install dependencies (backend)
cd backend
pip install -r requirements.txt

# Install dependencies (frontend)
cd ../web
npm install
```

### Development

```bash
# Run backend (API)
cd backend
uvicorn main:app --reload --port 8000

# Run frontend (Next.js)
cd web
npm run dev

# Build Chrome extension
cd extension
npm run build
```

## 📁 Project Structure

```
algoready/
├── README.md
├── LICENSE
├── .gitignore
├── docs/
│   ├── PROJECT-STATUS.md
│   └── DESIGN-SYSTEM.md
├── research/
│   ├── 01-public-website.md
│   ├── 02-extension-workflows.md
│   ├── 03-chart-overlay.md
│   ├── 04-strategy-workflows.md
│   ├── 05-zerodha.md
│   ├── 06-upstox.md
│   ├── 07-fyers.md
│   ├── 08-evidence-ledger.md
│   ├── 09-feature-matrix.md
│   └── 10-technical-specification.md
├── web/                    # Web application (Next.js + TypeScript)
│   ├── app/                # App Router pages
│   ├── components/         # React components
│   ├── lib/                # Utilities and hooks
│   ├── public/             # Static assets
│   ├── styles/             # Global styles
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── next.config.js
├── backend/               # Backend API (FastAPI + Python)
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/    # API endpoints
│   │   ├── auth/          # Authentication
│   │   ├── core/          # Core configuration
│   │   ├── db/            # Database setup
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   ├── strategies/    # Strategy implementations
│   │   └── main.py        # FastAPI app
│   ├── alembic/           # Database migrations
│   ├── requirements.txt
│   └── pyproject.toml
├── extension/             # Chrome Extension (Manifest V3)
│   ├── src/
│   │   ├── background/    # Service worker
│   │   ├── content/       # Content scripts
│   │   ├── popup/         # Popup UI
│   │   ├── sidepanel/     # Side panel UI
│   │   └── overlay/       # Chart overlay
│   ├── public/            # Styles, icons, web accessible
│   ├── manifest.json
│   └── package.json
└── docker-compose.yml
```

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Web Client    │     │ Chrome Extension│     │   Backend API   │
│   (Next.js)     │◄───►│   (React MV3)   │◄───►│   (FastAPI)     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
       │                        │                        │
       ▼                        ▼                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Database Layer                               │
│   PostgreSQL • Redis Cache                                      │
└─────────────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Service Layer                                │
│   Broker Services • Strategy Engine • Market Data              │
└─────────────────────────────────────────────────────────────────┘
```

## 🔌 Broker Integrations

| Broker | Status | Documentation |
|--------|--------|---------------|
| **Zerodha (Kite)** | ✅ Implemented | [kite.trade/docs](https://kite.trade/docs/connect/v3/) |
| **Upstox** | ✅ Implemented | [upstox.com/developer](https://upstox.com/developer/api-documentation/) |
| **FYERS** | ✅ Implemented | [myapi.fyers.in](https://myapi.fyers.in/docsv3/) |

Each broker has a dedicated adapter implementing:
- Authentication (OAuth 2.0)
- Position & holding retrieval
- Order placement, modification, cancellation
- Market quotes & historical data
- Instrument search

## 📊 Strategy Categories

| Category | Description |
|----------|-------------|
| **Scalping** | Quick trades on small price movements (EMA crossovers) |
| **Breakout** | Bollinger Band breakouts with volume confirmation |
| **Momentum** | RSI + MACD momentum shifts |
| **Reversion** | Mean reversion using Bollinger Bands & RSI |
| **Options** | Options strategies (straddles, spreads, etc.) |
| **Custom** | User-defined rule-based strategies |

### Built-in Strategies

1. **EMA Crossover Scalper** - 9/21 EMA crossover for quick scalps
2. **Bollinger Breakout** - Upper/lower band breaks with volume
3. **RSI Momentum** - RSI oversold/overbought + MACD confirmation
4. **Mean Reversion** - Price at bands with RSI extremes
5. **Custom Rule Builder** - Visual rule builder for custom strategies

## 🛡️ Security

- OAuth 2.0 for broker authentication
- JWT for API authentication
- HTTPS everywhere
- Encrypted token storage (AES-256)
- Rate limiting on API endpoints
- Input validation & sanitization
- CORS configured for production domains

## 📖 Documentation

- [Project Status](docs/PROJECT-STATUS.md)
- [Design System](docs/DESIGN-SYSTEM.md)
- [API Reference](backend/app/api/README.md)
- [Strategy Guide](docs/STRATEGY-GUIDE.md)
- [Extension Guide](docs/EXTENSION-GUIDE.md)
- [Deployment Guide](docs/DEPLOYMENT.md)

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd web
npm test

# Extension tests
cd extension
npm test
```

## 🐳 Docker Deployment

```bash
# Build and run all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## ☁️ Cloudflare Pages Deployment

The web application is deployed to: **https://algoready.pages.dev**

### Deployment Steps

1. Connect GitHub repository to Cloudflare Pages
2. Build command: `npm run build`
3. Build output directory: `web/.next`
4. Environment variables:
   - `NEXT_PUBLIC_API_URL`: Backend API URL
   - `NEXT_PUBLIC_WS_URL`: WebSocket URL

## 🤝 Contributing

We welcome contributions! Please read our [contributing guidelines](CONTRIBUTING.md) before submitting a pull request.

### Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

AlgoReady is a trading platform that connects to broker APIs. Trading involves significant risk of loss and is not suitable for all investors. Past performance is not indicative of future results. This platform is for educational and informational purposes only. Always perform your own due diligence before trading. Consult a qualified financial advisor before making investment decisions.

---

## 📦 Package Information

### Backend (FastAPI)

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | 0.109+ | Web framework |
| uvicorn | 0.27+ | ASGI server |
| sqlalchemy | 2.0+ | ORM |
| alembic | 1.13+ | Migrations |
| pydantic | 2.5+ | Validation |
| python-jose | 3.3+ | JWT |
| passlib | 1.7+ | Password hashing |
| httpx | 0.26+ | HTTP client |
| pandas | 2.2+ | Data analysis |
| numpy | 1.26+ | Numerical computing |

### Frontend (Next.js)

| Package | Version | Purpose |
|---------|---------|---------|
| next | 15.2+ | React framework |
| react | 18.3+ | UI library |
| tailwindcss | 3.4+ | Styling |
| zustand | 4.5+ | State management |
| axios | 1.7+ | HTTP client |
| @tradingview/lightweight-charts | 4.5+ | Charting |
| lucide-react | 0.44+ | Icons |

### Extension (Chrome MV3)

| Package | Version | Purpose |
|---------|---------|---------|
| React | 18.3+ | UI library |
| TypeScript | 5.5+ | Type safety |
| Vite | 5.0+ | Build tool |
| Tailwind CSS | 3.4+ | Styling |

---

**Ready to start trading smarter? Let's build AlgoReady together!** 🚀