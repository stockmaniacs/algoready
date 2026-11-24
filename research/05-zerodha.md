# AlgoReady Research - Zerodha Integration

**Date**: 2026-11-24
**Investigator**: OpenCode AI Agent
**Purpose**: Investigation of Zerodha Kite API for broker integration

---

## CONFIRMED FINDINGS

### Introduction
- **API Name**: Kite Connect 3
- **Developer Portal**: https://developers.kite.trade/
- **Documentation**: https://kite.trade/docs/connect/v3/

**Status**: CONFIRMED

### Prerequisites
- Active Zerodha trading account with 2FA TOTP enabled
- Developer account at Kite Connect Developer Portal
- API credentials (api_key, api_secret)
- Configured redirect URL for OAuth flow

**Status**: CONFIRMED

### Authentication Flow
- **OAuth 2.0 Implementation**: Standard OAuth 2.0 Authorization Code flow
- **Login Flow URL**: `https://kite.trade/connect/login?v=3&api_key=<api_key>&redirect_uri=<redirect_uri>`
- **Token Exchange**: POST to `https://api.kite.trade/rops/token` to exchange request_token for access_token
- **Access Token**: Valid for session lifetime (typically expires at EOD or on logout)
- **Request Token**: Single-use, expires in 30 seconds

**Status**: CONFIRMED

### API Endpoints

#### User Endpoints
- `GET /api/v2/user/profile` - Get user profile
- `GET /api/v2/user/metrics` - Get user metrics
- `GET /api/v2/login` - Login URL generation

#### Orders
- `GET /api/v2/orders` - List all orders
- `GET /api/v2/orders/<order_id>` - Get order details
- `POST /api/v2/orders` - Place new order
- `PUT /api/v2/orders/<order_id>` - Modify order
- `DELETE /api/v2/orders/<order_id>` - Cancel order
- `GET /api/v2/orders/batch` - Batch order operations

**Status**: CONFIRMED

#### Positions
- `GET /api/v2/positions` - Get all positions
- `GET /api/v2/positions/portfolio` - Get portfolio positions
- `POST /api/v2/positions` - Exit position

#### Portfolio
- `GET /api/v2/portfolio/holdings` - Get holdings
- `GET /api/v2/portfolio/positions` - Get positions
- `POST /api/v2/portfolio/margins` - Calculate margin

#### Market Data
- `GET /api/v2/instruments/<exchange>` - List instruments
- `GET /api/v2/quote` - Get quotes for multiple instruments
- `GET /api/v2/quote/<exchange>/<trading_symbol>` - Get quote for single instrument
- `GET /api/v2/historical/<instrument_token>/<from>/<to>/<interval>` - Historical data
- `GET /api/v2/quotes` - Bulk quotes
- `GET /api/v2/ltp` - Last traded price

#### WebSocket Streaming
- **Connection URL**: `wss://ws.kite.trade`
- **Authentication**: Send access token upon connection
- **Modes**:
  - Mode 1: LTP (Last Traded Price)
  - Mode 2: Quote (Full market depth)
  - Mode 3: Full (LTP + OHLC + Volume)
- **Topics**:
  - `nws_<exchange>_<instrument_token>` - Market data
  - `nws_positions` - Position updates
  - `nws_orders` - Order updates
  - `nws_triggered_orders` - Triggered orders

**Status**: CONFIRMED

#### Other
- `GET /api/v2/lots` - Get lot size information
- `GET /api/v2/margins` - Get margin information
- `GET /api/v2/margins/<exchange>` - Get margins for exchange
- `GET /api/v2/income` - Get profit and loss
- `GET /api/v2/claims` - Get margin claims

**Status**: CONFIRMED

### Order Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| tradingsymbol | string | Yes | Trading symbol (e.g., "ACC") |
| exchange | string | Yes | Exchange (NSE, BSE, NSE-CM, NSE-FO, BSE-CM, BSE-FO) |
| transaction_type | string | Yes | BUY or SELL |
| order_type | string | Yes | MARKET, LIMIT, SL-MARKET, SL-LIMIT |
| product | string | Yes | CNC, MOM, CO, MIS, NRML |
| quantity | integer | Yes | Order quantity |
| price | number | Conditional | Required for LIMIT/SL-LIMIT orders |
| validity | string | No | DAY or GTC |
| variety | string | No | regular, amo, ice, iif |
| squareoff | number | No | Squareoff price for bracket orders |
| trailing_stop | number | No | Trailing stoploss value |

**Status**: CONFIRMED

### Response Structure
- All responses in JSON format
- Success: HTTP 200
- Error: JSON with "error" and "message" fields
- Standard error codes documented

**Status**: CONFIRMED

---

## INFERRED FINDINGS

### Instrument Format
- Uses numeric `instrument_token` for internal identification
- `tradingsymbol` for human-readable symbol (e.g., "RELIANCE-EQ", "NIFTY23JUL60000CALL")
- Exchange codes: NSE, BSE, NFO, BFO, MSE, MCX, NSEL, BSELN, BSEFO, NSEL, BSELC

**Status**: INFERRED from documentation examples

### Order Product Types
- **CNC**: Cash and Carry (Equity delivery)
- **MIS**: Margin Intraday Square Off (Intraday)
- **NRML**: Normal (overnight positions)
- **CO**: Cover Order (with squareoff)
- **BO**: Bracket Order (with SL and target)

**Status**: INFERRED from API documentation

### Market Data Subscription
- WebSocket requires subscription to specific topics
- Supports multiple modes for different data needs
- Rate limiting applies to WebSocket connections

**Status**: INFERRED from WebSocket documentation

### Session Management
- Access tokens expire at end of trading session
- Refresh tokens not provided in standard flow
- Need to re-authenticate for each session

**Status**: INFERRED from authentication documentation

---

## UNKNOWN FINDINGS

### Rate Limits
- Exact API rate limits not fully documented in public docs
- WebSocket connection limits unclear

**Status**: UNKNOWN

### Error Handling Details
- Specific error codes and their meanings
- Retry logic implementation

**Status**: UNKNOWN

### Order Validation Rules
- Exact validation logic for different order types
- Complex product type validation

**Status**: UNKNOWN

### WebSocket Reconnection Logic
- Recommended reconnection strategy
- Heartbeat mechanisms
- Session recovery procedures

**Status**: UNKNOWN

---

## NOT ACCESSIBLE FINDINGS

### Private API Endpoints
- Any undocumented endpoints used by Zing Trade extension
- Internal broker APIs not publicly documented

**Status**: NOT ACCESSIBLE

### Proprietary Algorithm Implementations
- Zerodha's internal matching engine
- Risk management algorithms
- Order routing logic

**Status**: NOT ACCESSIBLE

---

## IMPLEMENTATION NOTES FOR ALGOREADY

### Authentication Flow (Recommended)
1. User visits `/auth/zerodha` endpoint
2. Server redirects to Zerodha login with generated state
3. User authenticates and authorizes
4. Redirect back with `code` parameter
5. Server exchanges `code` for `access_token`
6. Store encrypted access_token in database
7. Return access_token to client (if needed for direct connection)

### WebSocket Connection (Recommended)
1. Use server-side WebSocket proxy
2. Authenticate connection with access_token
3. Route market data to client via own WebSocket
4. Handle reconnections and session recovery

### Security Considerations
- Never expose `api_secret` to client
- Always verify `state` parameter in OAuth callback
- Store tokens encrypted at rest
- Implement proper token refresh logic

---

## LIMITATIONS

1. **End-of-Day Token Expiry**: Access tokens expire at end of trading day
2. **No Refresh Tokens**: Full re-authentication required each session
3. **Rate Limits**: Subject to Zerodha's API rate limits
4. **Market Hours**: APIs primarily functional during market hours

---

## REFERENCES

- Official Documentation: https://kite.trade/docs/connect/v3/
- Developer Portal: https://developers.kite.trade/
- Status Page: https://kite.trade/status/
- Community Forum: https://kite.trade/forum/

---

**Evidence Status**: Phase 2E Complete
**Last Updated**: 2026-11-24