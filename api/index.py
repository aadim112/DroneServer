from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from datetime import datetime

app = FastAPI(title="Drone Alert API", version="1.0.0")

# Add CORS middleware
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
        "version": "1.0.0",
        "status": "running",
        "deployment": "vercel-api",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "deployment": "vercel-api",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/alerts")
async def get_alerts():
    """Get all alerts"""
    return {
        "alerts": [],
        "count": 0,
        "message": "No alerts found"
    }

@app.post("/api/alerts")
async def create_alert(alert_data: dict):
    """Create a new alert"""
    return {
        "message": "Alert created successfully",
        "alert_id": "test_alert_001",
        "data": alert_data,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/stats")
async def get_stats():
    """Get system stats"""
    return {
        "total_alerts": 0,
        "active_drones": 0,
        "system_status": "operational",
        "timestamp": datetime.utcnow().isoformat()
    }

# Export for Vercel
app.debug = True 