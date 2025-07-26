#!/usr/bin/env python3
"""
Minimal Railway App - Guaranteed to Work
"""

import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Create minimal FastAPI app
app = FastAPI(title="Drone Alert System", version="1.0.0")

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Drone Alert Management System",
        "status": "running",
        "deployment": "minimal"
    }

@app.get("/health")
async def health():
    """Simple health check"""
    return {
        "status": "healthy",
        "message": "Service is running"
    }

@app.get("/api/alerts")
async def get_alerts():
    """Get alerts endpoint"""
    return {
        "alerts": [],
        "count": 0,
        "message": "Minimal deployment - database not connected"
    }

@app.post("/api/alerts")
async def create_alert():
    """Create alert endpoint"""
    return {
        "alert_id": "minimal_alert_001",
        "message": "Alert created (minimal deployment)"
    }

@app.get("/api/stats")
async def get_stats():
    """Get stats endpoint"""
    return {
        "status": "minimal",
        "connections": 0,
        "message": "Minimal deployment active"
    }

if __name__ == "__main__":
    # Get port from environment (Railway sets this)
    port = int(os.getenv("PORT", 8000))
    
    print(f"🚀 Starting minimal Railway app on port {port}")
    print(f"🌐 Health check: http://0.0.0.0:{port}/health")
    
    # Start server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    ) 