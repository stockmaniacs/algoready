# AlgoReady Research - Upstox Integration

**Date**: 2026-11-24
**Investigator**: OpenCode AI Agent
**Purpose**: Investigation of Upstox API for broker integration

---

## CONFIRMED FINDINGS

### Introduction
- **API Name**: Upstox API
- **Developer Portal**: https://account.upstox.com/developer/apps
- **Documentation**: https://upstox.com/developer/api-documentation/

**Status**: CONFIRMED

### Prerequisites
- Active Upstox trading account
- Developer account at Upstox Developer Portal
- API Key and Secret from app creation
- Configured redirect URL for OAuth flow

**Status**: CONFIRMED

### Authentication Flow
- **OAuth 2.0 Implementation**: Authorization Code Grant Flow
- **Authorization URL**: `https://api.upstox.org/v2/login/authorization`
- **Token Exchange**: POST to `https://api.upstox.org/v2/login/token`
- **Access Token**: Bearer token for API authentication
- **Refresh Token**: Provided for token refresh (implementation varies)

**Status**: CONFIRMED

### API Endpoints

#### User Endpoints
- `GET /v2/user/profile` - Get user profile
- `GET /v2/user/trading-credentials` - Get trading credentials

#### Orders
- `GET /v2/orders` - List all orders
- `GET /v2/orders/{order_id}` - Get order details
- `POST /v2/orders` - Place new order
- `PUT /v2/orders/{order_id}` - Modify order
- `DELETE /v2/orders/{order_id}` - Cancel order

#### Positions
- `GET /v2/positions` - Get all positions
- `GET /v2/positions/history` - Get position history

#### Portfolio
- `GET /v2/portfolio/holdings` - Get holdings
- `GET /v2/portfolio/positions` - Get positions
- `GET /v2/portfolio/margins` - Get margin information

#### Market Data
- `GET /v2/quote/ohlc` - Get OHLC data
- `GET /v2/quote` - Get quotes for instruments
- `GET /v2/quote/{instrument_key}` - Get quote for single instrument
- `GET /v2/instruments/{exchange}` - List instruments for exchange
- `GET /v2/historical-data/{instrument_key}/{interval}/{from}/{to}` - Historical data

#### WebSocket Streaming
- **Connection URL**: `wss://ws.upstox.org`
- **Authentication**: Access token in query parameter
- **Topics Available**:
  - Market data feeds
  - Order updates
  - Position updates

**Status**: CONFIRMED

### Order Parameters Structure

#### Order Request Body
```json
{
  "order_type": "LIMIT",
  "product_type": "INTRADAY",
  "duration": "DAY",
  "instrument_token": "NSE:RELIANCE",
  "quantity": "1",
  "price": "2500",
  "transaction_type": "BUY"
}
```

**Status**: CONFIRMED

### Response Formats
- All responses in JSON format
- Success: HTTP 2xx status codes
- Error: JSON with error details
- Standardized error response structure

**Status**: CONFIRMED

---

## INFERRED FINDINGS

### Instrument Format
- Uses `instrument_key` format: `<exchange>:<symbol>`
- Example: `NSE:RELIANCE`, `NSE:NIFTY`, `BSE:ACC`
- Exchange prefixes: NSE, BSE, NFO, BFO, MCX, NSEL, BSELN

**Status**: INFERRED from documentation examples

### Product Types
- **INTRADAY**: Intraday trading
- **CASH**: Cash (delivery) trades
- **COVER**: Cover orders
- **MARGIN**: Margin trading

**Status**: INFERRED from API documentation

### Order Types
- **LIMIT**: Limit order
- **MARKET**: Market order
- **SL-MARKET**: Stop loss market order
- **SL-LIMIT**: Stop loss limit order

**Status**: INFERRED from API documentation

### WebSocket Subscription Format
- Subscribe to topics using instrument keys
- Separate topics for market data, orders, positions

**Status**: INFERRED from WebSocket documentation

### Session Management
- Access tokens have expiration (typically 1 hour)
- Refresh token flow for obtaining new access tokens
- Proper token management required

**Status**: INFERRED from OAuth standard patterns

---

## UNKNOWN FINDINGS

### Exact Rate Limits
- API rate limits not fully specified
- WebSocket connection limits unclear

**Status**: UNKNOWN

### Order Validation Rules
- Exact validation logic for different order types
- Complex product type validation
- Exchange-specific restrictions

**Status**: UNKNOWN

### Historical Data Availability
- Lookback period for historical data
- Interval options for candles
- Data quality and completeness

**Status**: UNKNOWN

### WebSocket Reconnection Strategy
- Recommended reconnection logic
- Session recovery mechanisms
- Heartbeat configuration

**Status**: UNKNOWN

---

## NOT ACCESSIBLE FINDINGS

### Private API Endpoints
- Any undocumented endpoints used by applications
- Internal authentication flows
- Proprietary broker algorithms

**Status**: NOT ACCESSIBLE

### Proprietary Algorithm Implementations
- Order routing logic
- Risk management systems
- Matching engine details

**Status**: NOT ACCESSIBLE

---

## IMPLEMENTATION NOTES FOR ALGOREADY

### Authentication Flow (Recommended)
1. User visits `/auth/upstox` endpoint
2. Server redirects to Upstox authorization with state parameter
3. User authenticates and authorizes application
4. Redirect back with authorization code
5. Server exchanges code for access_token and refresh_token
6. Store tokens securely (encrypted)
7. Use access_token for subsequent API calls

### WebSocket Implementation (Recommended)
1. Use server-side WebSocket proxy
2. Authenticate connection with access_token
3. Route market data to clients via own WebSocket
4. Handle reconnections gracefully

### Security Considerations
- Never expose API key and secret to client
- Verify state parameter in OAuth callback
- Store tokens encrypted at rest
- Implement proper token refresh logic
- Use HTTPS for all communications

---

## LIMITATIONS

1. **Rate Limiting**: Subject to Upstox API rate limits
2. **Token Expiration**: Access tokens expire, need refresh
3. **Market Hours**: APIs functional during market hours
4. **Instrument Availability**: Limited to supported exchanges

---

## REFERENCES

- Official Documentation: https://upstox.com/developer/api-documentation/
- Developer Portal: https://account.upstox.com/developer/apps
- Status Page: Not publicly available
- Community Forum: https://community.upstox.com/c/developer-api

---

**Evidence Status**: Phase 2E Complete
**Last Updated**: 2026-11-24