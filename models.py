from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime
from enum import Enum

class AlertStatus(str, Enum):
    PENDING = "pending"
    RESPONDED = "responded"
    COMPLETED = "completed"

class Alert(BaseModel):
    alert: str = Field(..., description="Alert description (e.g., 'Casualty - Person Detected')")
    drone_id: str = Field(..., description="ID of the drone that sent the alert")
    alert_location: Tuple[float, float, float] = Field(..., description="Alert location coordinates (x, y, z)")
    image: Optional[str] = Field(None, description="Image data or reference")
    image_received: int = Field(default=0, description="Image received status (0=no image, 1=received)")
    rl_responsed: int = Field(default=0, description="RL response status (0=no response, 1=responded)")
    score: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    timestamp: str = Field(..., description="Alert timestamp in ISO format")

class AlertCreate(BaseModel):
    alert: str
    drone_id: str
    alert_location: Tuple[float, float, float]
    image: Optional[str] = None
    image_received: int = 0
    rl_responsed: int = 0
    score: float
    timestamp: str

class AlertResponse(BaseModel):
    alert_id: str
    rl_responsed: int = 1

class AlertImageUpdate(BaseModel):
    alert_id: str
    image: str
    image_received: int = 1

class WebSocketMessage(BaseModel):
    type: str
    data: Dict[str, Any]
    client_type: str  # "drone" or "application"

class DroneCommand(BaseModel):
    alert_id: str
    command: str
    parameters: Optional[Dict[str, Any]] = None

class ConnectionInfo(BaseModel):
    client_id: str
    client_type: str
    connected_at: datetime 