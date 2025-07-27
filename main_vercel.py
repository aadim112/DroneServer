import asyncio
import logging
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import json
from typing import List, Dict, Any

from config import Config
from database import db_manager
from models import AlertCreate, AlertResponse, AlertImageUpdate

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for Vercel"""
    logger.info("Starting Drone Alert Management System on Vercel...")
    
    # Connect to database
    try:
        await db_manager.connect()
        logger.info("Database connected successfully")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
    
    yield
    
    # Disconnect from database
    try:
        await db_manager.disconnect()
        logger.info("Database disconnected")
    except Exception as e:
        logger.error(f"Error disconnecting from database: {e}")

# Create FastAPI app
app = FastAPI(
    title="Drone Alert Management System",
    description="Real-time drone alert management API",
    version="1.0.0",
    lifespan=lifespan
)

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
        "deployment": "vercel",
        "endpoints": {
            "api_docs": "/docs",
            "health": "/health",
            "alerts": "/api/alerts",
            "stats": "/api/stats"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        if db_manager.is_connected:
            # Try a simple database operation
            await db_manager.get_all_alerts(limit=1)
            db_status = "connected"
        else:
            db_status = "disconnected"
    except Exception as e:
        db_status = f"error: {str(e)[:50]}"
    
    return {
        "status": "healthy",
        "database": db_status,
        "deployment": "vercel",
        "timestamp": "2025-07-27T13:15:00Z"
    }

@app.get("/api/alerts")
async def get_alerts(limit: int = 100):
    """Get all alerts via REST API"""
    try:
        alerts = await db_manager.get_all_alerts(limit=limit)
        return {"alerts": alerts, "count": len(alerts)}
    except Exception as e:
        logger.error(f"Error getting alerts: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/alerts/{alert_id}")
async def get_alert(alert_id: str):
    """Get a specific alert by ID"""
    try:
        alert = await db_manager.get_alert(alert_id)
        if not alert:
            raise HTTPException(status_code=404, detail="Alert not found")
        return alert
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting alert {alert_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/alerts")
async def create_alert(alert: AlertCreate):
    """Create a new alert via REST API"""
    try:
        alert_data = alert.dict()
        alert_id = await db_manager.insert_alert(alert_data)
        return {
            "alert_id": alert_id, 
            "message": "Alert created successfully",
            "deployment": "vercel"
        }
    except Exception as e:
        logger.error(f"Error creating alert: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/api/alerts/{alert_id}/response")
async def update_alert_response(alert_id: str, response: AlertResponse):
    """Update alert response via REST API"""
    try:
        update_data = {
            'rl_responsed': response.rl_responsed,
            'status': 'responded'
        }
        
        success = await db_manager.update_alert(alert_id, update_data)
        if not success:
            raise HTTPException(status_code=404, detail="Alert not found")
        
        return {"message": "Alert response updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating alert response: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/api/alerts/{alert_id}/image")
async def update_alert_image(alert_id: str, image_update: AlertImageUpdate):
    """Update alert image via REST API"""
    try:
        update_data = {
            'image_received': image_update.image_received,
            'image': image_update.image,
            'status': 'completed'
        }
        
        success = await db_manager.update_alert(alert_id, update_data)
        if not success:
            raise HTTPException(status_code=404, detail="Alert not found")
        
        return {"message": "Alert image updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating alert image: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/stats")
async def get_system_stats():
    """Get system statistics"""
    try:
        return {
            "database_connected": db_manager.is_connected,
            "deployment": "vercel",
            "status": "healthy"
        }
    except Exception as e:
        logger.error(f"Error getting system stats: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Vercel requires this for serverless deployment
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000))) 