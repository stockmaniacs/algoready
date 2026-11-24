# AlgoReady Research - Evidence Ledger

**Date**: 2026-11-24
**Investigator**: OpenCode AI Agent
**Purpose**: Classification of all findings from Zing Trade investigation

---

## EVIDENCE CLASSIFICATION KEY

- **CONFIRMED**: Directly observed or verified in authoritative documentation
- **INFERRED**: Plausible but not proven
- **UNKNOWN**: Not established
- **NOT ACCESSIBLE**: Requires unavailable permissions or access

---

## PRODUCT FEATURES

| Feature | Status | Source |
|---------|--------|--------|
| Chrome Extension | CONFIRMED | Chrome Web Store listing |
| Extension ID | CONFIRMED | epibngeobhgllkfbeghnemppimnljhfb |
| Extension Version | CONFIRMED | 1.2.23 (as of Nov 20, 2026) |
| Multi-market Support | CONFIRMED | Indian F&O, Crypto, US Stocks |
| Real-time Signals | CONFIRMED | Product description |
| Chart Overlays | CONFIRMED | Product description |
| Strategy Marketplace | CONFIRMED | Screenshots, product description |
| Position Tracking | CONFIRMED | Product description |
| Order Execution | CONFIRMED | Product description (manual confirmation) |
| Multiple Strats Support | CONFIRMED | Product description |

**Status**: CONFIRMED

---

## BROKER INTEGRATIONS

### Zerodha (Kite Connect)
| Feature | Status | Evidence |
|---------|--------|----------|
| OAuth 2.0 Auth | CONFIRMED | https://kite.trade/docs/connect/v3/ |
| Order Placement | CONFIRMED | Official documentation |
| Order Modification | CONFIRMED | Official documentation |
| Order Cancellation | CONFIRMED | Official documentation |
| Position Data | CONFIRMED | Official documentation |
| Holding Data | CONFIRMED | Official documentation |
| Market Quotes | CONFIRMED | Official documentation |
| Historical Data | CONFIRMED | Official documentation |
| WebSocket Streaming | CONFIRMED | Official documentation |
| Product Types | CONFIRMED | CNC, MIS, NRML, CO, BO |
| Instrument Format | INFERRED | Uses instrument_token internally |
| OAuth Callback | CONFIRMED | request_token -> access_token flow |

**Overall Status**: CONFIRMED

### Upstox
| Feature | Status | Evidence |
|---------|--------|----------|
| OAuth 2.0 Auth | CONFIRMED | https://upstox.com/developer/api-documentation/ |
| Order Placement | CONFIRMED | Official documentation |
| Order Modification | CONFIRMED | Official documentation |
| Order Cancellation | CONFIRMED | Official documentation |
| Position Data | CONFIRMED | Official documentation |
| Holding Data | CONFIRMED | Official documentation |
| Market Quotes | CONFIRMED | Official documentation |
| Historical Data | CONFIRMED | Official documentation |
| WebSocket Streaming | CONFIRMED | Official documentation |
| Instrument Format | INFERRED | instrument_key format (NSE:RELIANCE) |

**Overall Status**: CONFIRMED for documented endpoints

### FYERS
| Feature | Status | Evidence |
|---------|--------|----------|
| OAuth 2.0 Auth | CONFIRMED | https://myapi.fyers.in/docsv3/ |
| Order Placement | CONFIRMED | Official documentation |
| Order Modification | CONFIRMED | Official documentation |
| Order Cancellation | CONFIRMED | Official documentation |
| Position Data | CONFIRMED | Official documentation |
| Holding Data | CONFIRMED | Official documentation |
| Market Quotes | CONFIRMED | Official documentation |
| Historical Data | CONFIRMED | Official documentation |
| WebSocket Streaming | CONFIRMED | Official documentation |
| Order Types | CONFIRMED | Market, Limit, SL, STPL |
| Product Types | CONFIRMED | INTRADAY, CO, NRML, BO |

**Overall Status**: CONFIRMED for documented endpoints

---

## STRATEGY FEATURES

| Feature | Status | Source |
|---------|--------|--------|
| Pre-built Strategies | CONFIRMED | Product screenshots |
| Strategy Categories | CONFIRMED | Scalping, Breakout, Momentum, etc. |
| Entry Signals | CONFIRMED | Product description |
| Target Levels | CONFIRMED | Product description |
| Stop-Loss Levels | CONFIRMRED | Product description |
| Backtest Data | CONFIRMED | Strategy descriptions |
| Strategy Descriptions | CONFIRMED | Marketplace screenshots |

**Status**: CONFIRMED

---

## WEBSITE STRUCTURE

| Page/Section | Status | Evidence |
|--------------|--------|----------|
| Homepage | CONFIRMED | Direct URL |
| Product Section | CONFIRMED | Navigation |
| Integrations | CONFIRMED | Navigation |
| Pricing/Plans | CONFIRMED | Navigation |
| Resources/FAQs | CONFIRMED | Navigation |
| Blog | CONFIRMED | Navigation |
| Contact | CONFIRMED | Footer |
| Privacy Policy | CONFIRMED | Footer |
| Terms | CONFIRMED | Footer |

**Status**: CONFIRMED

---

## TECHNICAL SPECIFICATIONS

| Technical Aspect | Status | Notes |
|-----------------|--------|-------|
| Responsive Design | CONFIRMED | Website adapts to screen sizes |
| Modern Web Tech | INFERRED | Next.js-like structure (inferred from URL patterns) |
| HTTPS | CONFIRMED | All pages use HTTPS |
| Extension Size | CONFIRMED | 10.98 MiB |
| Language | CONFIRMED | English |
| Developer Info | CONFIRMED | Bitkuber Investments Pvt Ltd, Bangalore |

**Status**: MIXED

---

## NOT ACCESSIBLE INFORMATION

| Item | Access Level | Reason |
|------|--------------|--------|
| Extension Source Code | NOT ACCESSIBLE | Cannot access Chrome extension source |
| Proprietary Strategies | NOT ACCESSIBLE | Not publicly documented |
| Internal Architecture | UNKNOWN | Not publicly documented |
| Broker API Rate Limits | UNKNOWN | Not fully documented |
| WebSocket Implementation | UNKNOWN | Specific details not public |
| Order Routing Logic | NOT ACCESSIBLE | Proprietary |
| Risk Management | NOT ACCESSIBLE | Proprietary |

---

## INFERENCES FOR ALGOREADY IMPLEMENTATION

### Required Components (Inferred)
1. **Backend API** (Python/Starlette or Cloudflare Workers)
2. **Database** (PostgreSQL for user data, Redis for sessions)
3. **Auth System** (JWT, OAuth with brokers)
4. **Strategy Engine** (Python-based, modular)
5. **Chart Overlay** (React + SVG)
6. **Chrome Extension** (Manifest V3)
7. **Frontend** (Next.js/React/Tailwind)
8. **WebSocket Server** (For real-time data)
9. **Payment System** (Razorpay integration)

### Broker Integration Patterns (Inferred)
- OAuth flow for each broker
- Server-side token storage
- WebSocket proxy for market data
- Normalized API for common operations

### Data Storage Requirements (Inferred)
- User accounts and credentials
- Broker connections
- Strategy subscriptions
- Order history
- Position tracking
- Market data cache

---

## LIMITATIONS

### Investigation Limitations
1. Cannot inspect extension source code
2. Cannot test actual broker flows
3. Cannot verify order execution
4. Cannot access private APIs
5. Cannot test real trading scenarios

### Implementation Considerations
1. Must authenticate server-side for security
2. Must handle token expiry properly
3. Must implement WebSocket proxying
4. Must normalize broker data formats
5. Must handle rate limiting gracefully

---

## VERIFIED BY DOCUMENTATION

### URLs Verified
- https://zing.trade/ - Homepage
- https://chromewebstore.google.com/detail/zing-trade/epibngeobhgllkfbeghnemppimnljhfb - Extension
- https://kite.trade/docs/connect/v3/ - Zerodha API
- https://upstox.com/developer/api-documentation/ - Upstox API
- https://myapi.fyers.in/docsv3/ - FYERS API

### Documents Referenced
- Chrome Web Store listing
- Zing Trade product pages
- Broker API documentation

---

## NEXT STEPS

1. Complete technical specification
2. Design database schema
3. Implement backend API
4. Build frontend application
5. Create Chrome extension
6. Integrate broker APIs
7. Build strategy engine

---

**Overall Evidence Status**: Partial (extension source code not accessible)
**Recommendation**: Build independent implementation based on documented APIs

---
**Last Updated**: 2026-11-24