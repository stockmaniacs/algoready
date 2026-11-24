"""Main FastAPI application for AlgoReady backend."""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import uvicorn
import os

# Import routers
from app.api.routes import auth, brokers, strategies, market, positions, orders

app = FastAPI(
    title="AlgoReady API",
    description="Backend API for AlgoReady trading platform",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://algoready.pages.dev",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(brokers.router, prefix="/api/v1/brokers", tags=["brokers"])
app.include_router(strategies.router, prefix="/api/v1/strategies", tags=["strategies"])
app.include_router(market.router, prefix="/api/v1/market", tags=["market"])
app.include_router(positions.router, prefix="/api/v1/positions", tags=["positions"])
app.include_router(orders.router, prefix="/api/v1/orders", tags=["orders"])


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "algoready-api"}


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to AlgoReady API",
        "version": "0.1.0",
        "docs": "/api/docs"
    }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )