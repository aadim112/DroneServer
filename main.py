import asyncio
import logging
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import json
from typing import List, Dict, Any

from config import Config
from database import db_manager
from websocket_manager import websocket_manager
from models import AlertCreate, AlertResponse, AlertImageUpdate

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting Drone Alert Management System...")
    
    # Connect to database
    try:
        await db_manager.connect()
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        # Continue without database for now
    
    # Start change stream to watch for alert updates
    async def change_stream_callback(change_event: Dict[str, Any]):
        """Callback function for database change stream events"""
        try:
            # Broadcast the change to all connected applications
            await websocket_manager.broadcast_to_applications({
                "type": "alert_update",
                "change": change_event,
                "timestamp": change_event.get('timestamp')
            })
        except Exception as e:
            logger.error(f"Error in change stream callback: {e}")
    
    await db_manager.start_change_stream(change_stream_callback)
    
    logger.info("System started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Drone Alert Management System...")
    await db_manager.disconnect()
    logger.info("System shutdown complete")

# Create FastAPI app
app = FastAPI(
    title="Drone Alert Management System",
    description="Real-time drone alert management with WebSocket communication and MongoDB Change Streams",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
os.makedirs(Config.UPLOAD_DIR, exist_ok=True)

# Mount static files for uploaded images
app.mount("/uploads", StaticFiles(directory=Config.UPLOAD_DIR), name="uploads")

@app.get("/dashboard/")
async def dashboard():
    """Serve the dashboard"""
    from fastapi.responses import FileResponse
    return FileResponse("dashboard/index.html")

# Mount dashboard static files
app.mount("/dashboard", StaticFiles(directory="dashboard"), name="dashboard")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Drone Alert Management System",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "dashboard": "/dashboard/",
            "api_docs": "/docs",
            "health": "/health",
            "alerts": "/api/alerts",
            "stats": "/api/stats"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database_connected": db_manager.is_connected,
        "websocket_stats": websocket_manager.get_connection_stats()
    }

@app.websocket("/ws/drone/{drone_id}")
async def websocket_drone_endpoint(websocket: WebSocket, drone_id: str):
    """WebSocket endpoint for drone connections"""
    client_id = None
    try:
        # Connect the drone
        client_id = await websocket_manager.connect(websocket, "drone", drone_id)
        
        if not client_id:
            return
        
        logger.info(f"Drone {drone_id} connected via WebSocket")
        
        # Handle incoming messages
        while True:
            try:
                # Receive message
                data = await websocket.receive_text()
                message_data = json.loads(data)
                
                # Handle the message
                await websocket_manager.handle_websocket_message(client_id, message_data)
                
            except WebSocketDisconnect:
                break
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON received from drone {drone_id}")
                continue
            except Exception as e:
                logger.error(f"Error handling message from drone {drone_id}: {e}")
                continue
                
    except WebSocketDisconnect:
        logger.info(f"Drone {drone_id} disconnected")
    except Exception as e:
        logger.error(f"Error in drone WebSocket connection: {e}")
    finally:
        if client_id:
            await websocket_manager.disconnect(client_id)

@app.websocket("/ws/application/{app_id}")
async def websocket_application_endpoint(websocket: WebSocket, app_id: str):
    """WebSocket endpoint for application connections"""
    client_id = None
    try:
        # Connect the application
        client_id = await websocket_manager.connect(websocket, "application", app_id)
        
        if not client_id:
            return
        
        logger.info(f"Application {app_id} connected via WebSocket")
        
        # Send current alerts to the new application
        try:
            alerts = await db_manager.get_all_alerts(limit=50)
            if alerts:
                initial_data_message = {
                    "type": "initial_alerts",
                    "alerts": alerts,
                    "timestamp": asyncio.get_event_loop().time()
                }
                await websocket_manager.send_personal_message(client_id, initial_data_message)
        except Exception as e:
            logger.error(f"Error sending initial alerts to application {app_id}: {e}")
        
        # Handle incoming messages
        while True:
            try:
                # Receive message
                data = await websocket.receive_text()
                message_data = json.loads(data)
                
                # Handle the message
                await websocket_manager.handle_websocket_message(client_id, message_data)
                
            except WebSocketDisconnect:
                break
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON received from application {app_id}")
                continue
            except Exception as e:
                logger.error(f"Error handling message from application {app_id}: {e}")
                continue
                
    except WebSocketDisconnect:
        logger.info(f"Application {app_id} disconnected")
    except Exception as e:
        logger.error(f"Error in application WebSocket connection: {e}")
    finally:
        if client_id:
            await websocket_manager.disconnect(client_id)

# REST API endpoints for additional functionality

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
        return {"alert_id": alert_id, "message": "Alert created successfully"}
    except Exception as e:
        logger.error(f"Error creating alert: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/api/alerts/{alert_id}/response")
async def update_alert_response(alert_id: str, response: AlertResponse):
    """Update alert response via REST API"""
    try:
        update_data = {
            'response': response.response,
            'actions': response.actions,
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
            'image_url': image_update.image_url,
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
        stats = websocket_manager.get_connection_stats()
        return {
            "websocket_stats": stats,
            "database_connected": db_manager.is_connected
        }
    except Exception as e:
        logger.error(f"Error getting system stats: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/debug/env")
async def debug_environment():
    """Debug endpoint to show environment variables (for troubleshooting)"""
    import os
    return {
        "MONGODB_URI_set": bool(os.getenv('MONGODB_URI')),
        "DATABASE_NAME_set": bool(os.getenv('DATABASE_NAME')),
        "HOST_set": bool(os.getenv('HOST')),
        "PORT_set": bool(os.getenv('PORT')),
        "ENVIRONMENT_set": bool(os.getenv('ENVIRONMENT')),
        "DEBUG_set": bool(os.getenv('DEBUG')),
        "database_connected": db_manager.is_connected,
        "mongodb_uri_length": len(os.getenv('MONGODB_URI', '')) if os.getenv('MONGODB_URI') else 0,
        "database_name": os.getenv('DATABASE_NAME', 'NOT_SET'),
        "host": os.getenv('HOST', 'NOT_SET'),
        "port": os.getenv('PORT', 'NOT_SET')
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=True,
        log_level="info"
    ) 