# Deployment Guide

This guide covers deploying AlgoReady to production environments.

## 🌐 Cloudflare Pages (Frontend)

### Prerequisites

- Cloudflare account
- GitHub repository connected to Cloudflare Pages
- Node.js 18+ installed locally

### Setup Steps

1. **Connect Repository**
   - Go to Cloudflare Pages dashboard
   - Click "Create a project"
   - Connect your GitHub account
   - Select `stockmaniacs/algoready` repository

2. **Build Configuration**
   - Build command: `npm run build`
   - Build output directory: `web/.next`
   - Root directory: `web`
   - Node.js version: `18.x`

3. **Environment Variables**
   ```
   NEXT_PUBLIC_API_URL=https://api.algoready.dev
   NEXT_PUBLIC_WS_URL=wss://api.algoready.dev
   ```

4. **Custom Domain** (Optional)
   - Add `algoready.pages.dev` as custom domain
   - Configure DNS records as instructed

### Deployment

```bash
# Manual deployment via Wrangler
cd web
npm run build
npx wrangler pages deploy .next --project-name=algoready
```

### Auto-deployment

Cloudflare Pages automatically deploys on every push to `main` branch.

## 🐳 Docker Deployment (Backend + Frontend)

### Prerequisites

- Docker and Docker Compose installed
- Domain name with SSL certificates
- PostgreSQL and Redis (or use containers)

### Production docker-compose.yml

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: algoready
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: algoready
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    environment:
      DATABASE_URL: postgresql+asyncpg://algoready:${POSTGRES_PASSWORD}@postgres:5432/algoready
      REDIS_URL: redis://redis:6379/0
      SECRET_KEY: ${SECRET_KEY}
      ALGORITHM: HS256
      ACCESS_TOKEN_EXPIRE_MINUTES: 60
      REFRESH_TOKEN_EXPIRE_DAYS: 30
      CORS_ORIGINS: https://algoready.pages.dev
      ENVIRONMENT: production
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
    restart: unless-stopped

  frontend:
    build:
      context: ./web
      dockerfile: Dockerfile.prod
    environment:
      NEXT_PUBLIC_API_URL: https://api.algoready.dev
      NEXT_PUBLIC_WS_URL: wss://api.algoready.dev
    ports:
      - "3000:3000"
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

### Deploy

```bash
# Set environment variables
export POSTGRES_PASSWORD="secure_random_password"
export SECRET_KEY="secure_random_secret_key_32_chars_min"

# Start services
docker-compose -f docker-compose.yml up -d

# Run migrations
docker-compose exec backend alembic upgrade head

# Check logs
docker-compose logs -f
```

## 🔧 Backend Production Setup

### Environment Variables

Create `.env.production`:

```env
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/algoready
REDIS_URL=redis://host:6379/0
SECRET_KEY=your_32_character_minimum_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=30
CORS_ORIGINS=https://algoready.pages.dev
ENVIRONMENT=production

# Broker API Keys (for server-side operations)
ZERODHA_API_KEY=your_zerodha_api_key
ZERODHA_API_SECRET=your_zerodha_api_secret
UPSTOX_API_KEY=your_upstox_api_key
UPSTOX_API_SECRET=your_upstox_api_secret
FYERS_API_KEY=your_fyers_api_key
FYERS_API_SECRET=your_fyers_api_secret
```

### Database Migrations

```bash
# Run migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"
```

### SSL/HTTPS

Use a reverse proxy (Nginx, Traefik, or Caddy) for SSL termination:

```nginx
# Nginx example
server {
    listen 443 ssl http2;
    server_name api.algoready.dev;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## 📦 Chrome Extension Deployment

### Build Extension

```bash
cd extension
npm install
npm run build
```

### Chrome Web Store

1. Zip the `dist` folder
2. Go to [Chrome Web Store Developer Dashboard](https://chrome.google.com/webstore/developer/dashboard)
3. Click "New Item"
4. Upload the zip file
5. Fill in store listing details
6. Submit for review

### Manual Installation (Development)

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `dist` folder

## 🔐 Security Checklist

### Pre-deployment

- [ ] Generate strong `SECRET_KEY` (32+ chars)
- [ ] Use strong database passwords
- [ ] Enable SSL/TLS everywhere
- [ ] Configure CORS for production domains only
- [ ] Set up rate limiting
- [ ] Enable database SSL connections
- [ ] Use environment variables for all secrets
- [ ] Rotate API keys regularly
- [ ] Enable audit logging

### Post-deployment

- [ ] Monitor error rates
- [ ] Set up uptime monitoring
- [ ] Configure backup strategy for PostgreSQL
- [ ] Set up log aggregation
- [ ] Enable WAF rules
- [ ] Regular security scanning

## 📊 Monitoring

### Health Checks

```bash
# Backend health
curl https://api.algoready.dev/health

# Database connectivity
curl https://api.algoready.dev/api/v1/health/db

# Redis connectivity
curl https://api.algoready.dev/api/v1/health/redis
```

### Recommended Tools

- **Uptime**: UptimeRobot, Pingdom, or Cloudflare Health Checks
- **APM**: Datadog, New Relic, or Sentry
- **Logs**: Logtail, Papertrail, or ELK stack
- **Metrics**: Prometheus + Grafana

## 🔄 CI/CD Pipeline

### GitHub Actions Example

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
      - name: Install dependencies
        run: cd web && npm ci
      - name: Build
        run: cd web && npm run build
      - name: Deploy to Cloudflare Pages
        uses: cloudflare/pages-action@v1
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          projectName: algoready
          directory: web/.next

  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to server
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SERVER_SSH_KEY }}
          script: |
            cd /opt/algoready
            git pull
            docker-compose -f docker-compose.yml up -d --build
            docker-compose exec backend alembic upgrade head
```

## 🚨 Rollback Procedures

### Frontend (Cloudflare Pages)
- Go to Cloudflare Pages dashboard
- Click "Rollbacks"
- Select previous deployment
- Click "Rollback"

### Backend (Docker)
```bash
# Rollback to previous image
docker-compose pull
docker-compose up -d

# Or rollback database migration
alembic downgrade -1
```

## 📋 Environment-Specific Configurations

### Development
- `docker-compose.yml` (with hot reload)
- Local PostgreSQL/Redis
- Self-signed certificates

### Staging
- Separate namespace/cluster
- Production-like data (anonymized)
- Full monitoring enabled

### Production
- High availability setup
- Read replicas for database
- Redis cluster
- CDN for static assets
- WAF enabled

## 📞 Support

For deployment issues:
- Check logs: `docker-compose logs -f`
- Verify health endpoints
- Check Cloudflare Pages build logs
- Review GitHub Actions workflow runs