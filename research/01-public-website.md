# AlgoReady Research - Zing Trade Public Website

**Date**: 2026-11-24
**Investigator**: OpenCode AI Agent
**Purpose**: Independent investigation of publicly observable workflows and functionality

---

## CONFIRMED FINDINGS

### Homepage
- **URL**: https://zing.trade/
- **Primary Navigation**:
  - Home
  - Integrations
  - Product
  - Strategies
  - FAQs
  - Privacy Policy
  - Terms & Conditions
  - Risk Disclosure
  - Cancellation & Refund Policy

**Status**: CONFIRMED

### Hero Section
- **Tagline**: "Zing is a trading extension for Chrome that brings pre-built, backtested trading strategies directly to supported brokers and market charts."
- **Core Value Proposition**:
  - Real-time trading signals
  - One-click execution
  - Pre-built strategies
  - Works across platforms
- **Call-to-Action Buttons**: "Add Zing Extension", "Watch Demo"

**Status**: CONFIRMED

### Product Features Section
- **Real-Time Trading Signals**: Rule-based setups when predefined conditions are met
- **Entry, Target and Stop-Loss**: Complete trade structure preview
- **Pre-Built Strategy Access**: Ready-to-apply strategies without coding
- **Backtested Information**: Historical performance data
- **Streamlined Execution**: One-tap execution through connected provider
- **Multiple Strategies**: Monitor multiple strategies simultaneously
- **Live Position Tracking**: Track setups, positions, orders from one panel
- **Manual Control**: Review, modify, or reject every setup

**Status**: CONFIRMED

### Markets Covered
1. **Indian F&O**: NSE, BSE derivatives including Nifty, Bank Nifty, options, futures
2. **Cryptocurrencies**: Through available integrations
3. **US Stocks**: US-listed stocks

**Status**: CONFIRMED

### Supported Broker Integrations (Observable)
From screenshots and platform descriptions:
- **LEMONN**
- **DHAN**
- **ANGEL ONE**
- **KITEFYERS** (Zerodha integration via Kite)
- **FYERS**
- **UPSTOX**
- **GROWWINDMONEY**
- **INDMONEY**
- **COINSWITCH**
- **DELTA**
- **COINDCX**
- **BYBIT**
- **BINANCE**
- **SHARK EXCHANGE**
- **GIOTTUS**

**Status**: CONFIRMED

### Strategy Marketplace
- **Visible Strategies**:
  1. Scalping Pulse by Neeraj
  2. Prime Scalper EMA
  3. Inside Candle
  4. Mean Reversion Bollinger
  5. EMA Cross
  6. SwingKing Sniper
  7. Traffic Light
  8. Booming Bulls Supertrend
- **Strategy Details Displayed**: Name, creator, market type, entry/target/SL levels

**Status**: CONFIRMED

---

## INFERRED FINDINGS

### How Zing Works (Step-by-step Process)
1. **Add to Chrome**: Install extension and pin to toolbar
2. **Connect Account**: Link supported broker account
3. **Select Market**: Choose from Indian F&O, Crypto, or US Stocks
4. **Explore Marketplace**: Browse pre-built strategies
5. **Apply Strategy**: Select strategy for a chart
6. **Receive Signals**: Get structured trade setups
7. **Review & Confirm**: Verify Entry, Target, Stop-Loss
8. **Track Positions**: Monitor active trades

**Status**: INFERRED from workflow description

### User Requirements
- Chrome browser
- Active broker account
- Understanding of trading concepts
- 2FA TOTP enabled for some brokers
- Not designed for complete beginners

**Status**: INFERRED from product description

### Technical Architecture (Inferred)
- Chrome Extension (Manifest V3)
- Browser overlay technology
- WebSocket for real-time data
- OAuth for broker authentication
- Strategy engine running client-side

**Status**: INFERRED from product structure

---

## UNKNOWN FINDINGS

### Exact Pricing Plans
- Specific pricing for each tier
- Billing cycles
- Feature limitations per tier

**Status**: UNKNOWN - Waitlist model suggests custom pricing

### Authentication Flow Details
- Exact OAuth implementation
- Token storage mechanism
- Refresh token handling

**Status**: UNKNOWN - Requires extension analysis

### Broker API Integration Details
- Specific endpoints used
- Rate limiting implementation
- WebSocket connection handling

**Status**: UNKNOWN - Requires reverse engineering

### Strategy Implementation
- Strategy algorithms (proprietary)
- Signal generation logic
- Backtest methodology

**Status**: NOT ACCESSIBLE - Proprietary

### Chart Overlay Technology
- Overlay implementation
- Marker positioning algorithm
- Zoom/scroll handling

**Status**: UNKNOWN - Requires reverse engineering

---

## NOT ACCESSIBLE FINDINGS

### Proprietary Source Code
- Extension source code
- Strategy algorithms
- Backend API endpoints

**Status**: NOT ACCESSIBLE

### Private Credentials
- Broker API secrets
- Developer keys
- Authentication tokens

**Status**: NOT ACCESSIBLE

### Live Account Data
- User trading data
- Actual trades
- Performance metrics

**Status**: NOT ACCESSIBLE

### Private API Endpoints
- Internal backend APIs
- WebSocket private endpoints
- Authentication endpoints

**Status**: NOT ACCESSIBLE

---

## LIMITATIONS

1. **Public Data Only**: Cannot access authenticated sections without credentials
2. **Static Analysis**: Cannot observe real-time dynamic behavior
3. **No Code Access**: Cannot inspect source code or implementation
4. **No Credentials**: Cannot test with actual trading accounts
5. **No Live Trading**: Cannot verify actual execution flow

---

## OBSERVATION NOTES

### Branding Elements
- **Logo**: Zing Trade logo (visible in header and footer)
- **Color Scheme**: Blue/indigo primary, light background
- **Typography**: Clean, modern sans-serif

### Legal Disclaimers
- "Zing is a technology platform - not a SEBI-registered broker"
- "Not affiliated with or endorsed by third-party brokers"
- "Users execute trades through their respective broker accounts"
- "All broker names and logos belong to their respective owners"

### Key Messaging
- "Your next 100 trades are on us!" (Promotional offer)
- "No coding. No complicated algorithms. No separate terminal."
- "Review the structured setup, modify eligible details if required, and confirm the order yourself"
- "Zing is a signal and execution-assist platform, not an auto-trading bot"

---

## NEXT STEPS

1. Complete Chrome extension investigation
2. Investigate broker API integrations
3. Create independent implementation plan
4. Build AlgoReady platform

---

**Evidence Status**: Phase 2A Complete
**Last Updated**: 2026-11-24