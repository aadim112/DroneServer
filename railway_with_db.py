#!/usr/bin/env python3
"""
Railway App with Database Support - Store and View Posted Data
"""

import os
import sys
import json
from datetime import datetime
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Create FastAPI app
app = FastAPI(title="Drone Alert System", version="1.0.0")

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory database (will be lost on restart)
# In production, use MongoDB or PostgreSQL
alerts_db = []
alert_counter = 1

class AlertCreate(BaseModel):
    alert_type: str
    score: float
    location: str
    drone_id: str
    image_url: str = ""

class AlertResponse(BaseModel):
    alert_id: str
    actions: List[str]
    response: int = 1

class AlertImageUpdate(BaseModel):
    alert_id: str
    image_url: str
    image_received: int = 1

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Drone Alert Management System",
        "status": "running",
        "deployment": "with_database",
        "total_alerts": len(alerts_db),
        "endpoints": {
            "health": "/health",
            "alerts": "/api/alerts",
            "stats": "/api/stats",
            "view_data": "/api/view_data"
        }
    }

@app.get("/health")
async def health():
    """Simple health check"""
    return {
        "status": "healthy",
        "message": "Service is running",
        "database": "in_memory",
        "total_alerts": len(alerts_db)
    }

@app.get("/api/alerts")
async def get_alerts():
    """Get all alerts"""
    return {
        "alerts": alerts_db,
        "count": len(alerts_db),
        "message": f"Found {len(alerts_db)} alerts"
    }

@app.post("/api/alerts")
async def create_alert(alert: AlertCreate):
    """Create a new alert"""
    global alert_counter
    
    new_alert = {
        "alert_id": f"alert_{alert_counter:04d}",
        "alert_type": alert.alert_type,
        "score": alert.score,
        "image_url": alert.image_url,
        "location": alert.location,
        "drone_id": alert.drone_id,
        "timestamp": datetime.utcnow().isoformat(),
        "response": 0,
        "image_received": 0,
        "actions": []
    }
    
    alerts_db.append(new_alert)
    alert_counter += 1
    
    print(f"📊 New alert created: {new_alert['alert_id']}")
    
    return {
        "alert_id": new_alert["alert_id"],
        "message": "Alert created successfully",
        "alert": new_alert
    }

@app.put("/api/alerts/response")
async def update_alert_response(response: AlertResponse):
    """Update alert response"""
    for alert in alerts_db:
        if alert["alert_id"] == response.alert_id:
            alert["response"] = response.response
            alert["actions"] = response.actions
            alert["timestamp"] = datetime.utcnow().isoformat()
            
            print(f"📊 Alert response updated: {response.alert_id}")
            
            return {
                "alert_id": response.alert_id,
                "message": "Alert response updated successfully",
                "alert": alert
            }
    
    raise HTTPException(status_code=404, detail="Alert not found")

@app.put("/api/alerts/image")
async def update_alert_image(image_update: AlertImageUpdate):
    """Update alert image"""
    for alert in alerts_db:
        if alert["alert_id"] == image_update.alert_id:
            alert["image_url"] = image_update.image_url
            alert["image_received"] = image_update.image_received
            alert["timestamp"] = datetime.utcnow().isoformat()
            
            print(f"📊 Alert image updated: {image_update.alert_id}")
            
            return {
                "alert_id": image_update.alert_id,
                "message": "Alert image updated successfully",
                "alert": alert
            }
    
    raise HTTPException(status_code=404, detail="Alert not found")

@app.get("/api/stats")
async def get_stats():
    """Get system statistics"""
    total_alerts = len(alerts_db)
    pending_responses = len([a for a in alerts_db if a["response"] == 0])
    pending_images = len([a for a in alerts_db if a["image_received"] == 0])
    completed = len([a for a in alerts_db if a["response"] == 1 and a["image_received"] == 1])
    
    return {
        "status": "with_database",
        "total_alerts": total_alerts,
        "pending_responses": pending_responses,
        "pending_images": pending_images,
        "completed_alerts": completed,
        "message": "Database statistics"
    }

@app.get("/api/view_data")
async def view_data():
    """View all data in a formatted way"""
    if not alerts_db:
        return {
            "message": "No data available",
            "suggestion": "Create some alerts using POST /api/alerts"
        }
    
    formatted_alerts = []
    for alert in alerts_db:
        formatted_alert = {
            "ID": alert["alert_id"],
            "Type": alert["alert_type"],
            "Score": alert["score"],
            "Location": alert["location"],
            "Drone": alert["drone_id"],
            "Created": alert["timestamp"],
            "Response": "✅ Yes" if alert["response"] == 1 else "❌ No",
            "Image": "✅ Yes" if alert["image_received"] == 1 else "❌ No",
            "Actions": alert["actions"] if alert["actions"] else "None"
        }
        formatted_alerts.append(formatted_alert)
    
    return {
        "message": f"Found {len(alerts_db)} alerts",
        "data": formatted_alerts,
        "raw_data": alerts_db
    }

@app.delete("/api/alerts/{alert_id}")
async def delete_alert(alert_id: str):
    """Delete an alert"""
    for i, alert in enumerate(alerts_db):
        if alert["alert_id"] == alert_id:
            deleted_alert = alerts_db.pop(i)
            print(f"📊 Alert deleted: {alert_id}")
            return {
                "alert_id": alert_id,
                "message": "Alert deleted successfully",
                "deleted_alert": deleted_alert
            }
    
    raise HTTPException(status_code=404, detail="Alert not found")

@app.delete("/api/alerts")
async def clear_all_alerts():
    """Clear all alerts"""
    global alerts_db, alert_counter
    count = len(alerts_db)
    alerts_db = []
    alert_counter = 1
    
    print(f"📊 All {count} alerts cleared")
    
    return {
        "message": f"All {count} alerts cleared successfully",
        "remaining_alerts": 0
    }

if __name__ == "__main__":
    # Get port from environment (Railway sets this)
    port = int(os.getenv("PORT", 8000))
    
    print(f"🚀 Starting Railway app with database on port {port}")
    print(f"🌐 Health check: http://0.0.0.0:{port}/health")
    print(f"📊 View data: http://0.0.0.0:{port}/api/view_data")
    
    # Start server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    ) 