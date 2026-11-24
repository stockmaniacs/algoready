# AlgoReady Research - FYERS Integration

**Date**: 2026-11-24
**Investigator**: OpenCode AI Agent
**Purpose**: Investigation of FYERS API for broker integration

---

## CONFIRMED FINDINGS

### Introduction
- **API Name**: FYERS API v3
- **Developer Portal**: https://myapi.fyers.in/
- **Documentation**: https://myapi.fyers.in/docsv3/

**Status**: CONFIRMED

### Prerequisites
- Active FYERS trading account
- Developer account at FYERS API Portal
- App ID and App Secret from app creation
- Configured redirect URL for OAuth flow

**Status**: CONFIRMED

### Authentication Flow
- **OAuth 2.0 Implementation**: Authorization Code Grant Flow
- **Authorization URL**: `https://api.fyers.in/api/v2/authorize`
- **Token Exchange**: POST to `https://api.fyers.in/api/v2/session/token`
- **Access Token**: Bearer token for API authentication
- **Refresh Token**: Available for token refresh via `https://api.fyers.in/api/v2/passwd/token`

**Status**: CONFIRMED

### API Endpoints

#### Authentication
- `POST /api/v2/authorize` - Generate authorization code
- `POST /api/v2/session/token` - Exchange code for token
- `POST /api/v2/oauth/token` - Get fresh access token
- `POST /api/v2/passwd/token` - Refresh access token

#### Account Endpoints
- `GET /api/v2/accounts` - Get connected accounts
- `GET /api/v2/profile` - Get user profile
- `GET /api/v2/funds` - Get account funds
- `GET /api/v2/holdings` - Get holdings

#### Trading Endpoints
- `POST /api/v2/orders` - Place order
- `GET /api/v2/order-book` - Get order book
- `PUT /api/v2/orders/hedge` - Hedge order
- `DELETE /api/v2/order-book/{id}` - Cancel order
- `GET /api/v2/positions` - Get positions
- `GET /api/v2/positions/history` - Get position history

#### Market Data Endpoints
- `GET /api/v2/data/option-chain` - Get option chain
- `GET /api/v2/data/historical-data` - Get historical data
- `GET /api/v2/data/bulk-historical-data` - Bulk historical data
- `GET /api/v2/price-tokens` - Get price tokens
- `GET /api/v2/urls` - Get API URLs

#### WebSocket Streaming
- **Connection URL**: `wss://api.fyers.in/socket/v2`
- **Authentication**: Access token in query parameter
- **Topics Available**:
  - Market data (quotes, depth)
  - Order updates
  - Position updates

**Status**: CONFIRMED

### Order Parameters Structure

#### Order Request Body
```json
{
  "symbol": "NSE:RELIANCE",
  "qty": 1,
  "type": 1,
  "side": 1,
  "productType": 1,
  "limitPrice": 0,
  "stopPrice": 0,
  "priceFields": 1,
  "getOrderDetails": true
}
```

**Status**: CONFIRMED

### Order Types
- **type=1**: Market Order
- **type=2**: Limit Order
- **type=3**: Stop Loss Order
- **type=4**: Stop Loss Limit Order

### Product Types
- **productType=1**: INTRADAY
- **productType=2**: CO (Cover Order)
- **productType=3**: NRML (Normal/Delivery)
- **productType=4**: BO (Bracket Order)
- **productType=5**: IC (Intraday square off)

### Side (Transaction Type)
- **side=1**: BUY
- **side=2**: SELL

**Status**: CONFIRMED

### Response Formats
- All responses in JSON format
- Success: HTTP 200
- Error: JSON with "code" and "message" fields
- Standardized error handling

**Status**: CONFIRMED

---

## INFERRED FINDINGS

### Symbol Format
- Uses `EXCHANGE:SYMBOL` format
- Examples: `NSE:RELIANCE`, `BSE:ACC`, `NSE:NIFTY`, `NSE:BANKNIFTY`
- Option symbols: `NSE:RELIANCE-23-07-29-2900-C`

**Status**: INFERRED from documentation examples

### WebSocket Connection Process
1. Authenticate with access token
2. Subscribe to specific topics
3. Receive real-time data updates
4. Handle reconnections and session recovery

**Status**: INFERRED from WebSocket documentation

### Historical Data Availability
- Supports intraday (1min, 5min, 15min, 30min, 60min intervals)
- Daily candles available
- Options expiry data for expired contracts

**Status**: INFERRED from documentation structure

### Account Management
- Multiple accounts can be connected
- Account-level fund and position tracking
- Separate API tokens per account

**Status**: INFERRED from API structure

### Rate Limits
- Standard rate limits apply
- WebSocket connection limits for data streaming

**Status**: INFERRED from standard API practices

---

## UNKNOWN FINDINGS

### Exact Rate Limits
- API calls per minute/hour limits
- WebSocket message limits

**Status**: UNKNOWN

### Order Validation Rules
- Exact validation logic for different order types
- Exchange-specific restrictions and validations

**Status**: UNKNOWN

### Historical Data Coverage
- Exact lookback period
- Data quality and completeness
- Weekend/holiday data availability

**Status**: UNKNOWN

### WebSocket Reconnection Logic
- Recommended reconnection strategy
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
1. User visits `/auth/fyers` endpoint
2. Server redirects to FYERS authorization with state parameter
3. User authenticates and authorizes application
4. Redirect back with authorization code
5. Server exchanges code for access_token
6. Store access_token and refresh_token securely
7. Use access_token for subsequent API calls

### Token Refresh (Recommended)
1. Use refresh endpoint when access_token expires
2. Store new access_token
3. Continue using API with refreshed token

### WebSocket Implementation (Recommended)
1. Use server-side WebSocket proxy
2. Authenticate connection with access_token
3. Subscribe to required topics
4. Route data to clients via own WebSocket

### Security Considerations
- Never expose App Secret to client
- Verify state parameter in OAuth callback
- Store tokens encrypted at rest
- Implement proper token refresh logic
- Use HTTPS for all communications

---

## LIMITATIONS

1. **Rate Limiting**: Subject to FYERS API rate limits
2. **Token Expiration**: Access tokens expire, need refresh
3. **Market Hours**: APIs functional during market hours
4. **Symbol Format**: Requires proper exchange prefix

---

## REFERENCES

- Official Documentation: https://myapi.fyers.in/docsv3/
- Developer Portal: https://myapi.fyers.in/
- Status Page: Not publicly available
- Community Forum: https://community.fyers.in/

---

**Evidence Status**: Phase 2E Complete
**Last Updated**: 2026-11-24