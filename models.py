from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class AlertType(str, Enum):
    INTRUSION = "intrusion"
    FIRE = "fire"
    ACCIDENT = "accident"
    SECURITY_BREACH = "security_breach"
    ENVIRONMENTAL = "environmental"
    OTHER = "other"

class AlertStatus(str, Enum):
    PENDING = "pending"
    RESPONDED = "responded"
    COMPLETED = "completed"

class Alert(BaseModel):
    alert_id: str = Field(..., description="Unique alert identifier")
    alert_type: AlertType = Field(..., description="Type of alert")
    score: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    image_url: Optional[str] = Field(None, description="URL to alert image")
    location: Dict[str, float] = Field(..., description="GPS coordinates {lat, lng}")
    drone_id: str = Field(..., description="ID of the drone that sent the alert")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Alert timestamp")
    response: int = Field(default=0, description="Response status (0=no response, 1=responded)")
    image_received: int = Field(default=0, description="Image received status (0=no image, 1=received)")
    actions: Optional[List[str]] = Field(default=None, description="List of actions to be taken")
    status: AlertStatus = Field(default=AlertStatus.PENDING, description="Current alert status")
    description: Optional[str] = Field(None, description="Additional alert description")

class AlertCreate(BaseModel):
    alert_type: AlertType
    score: float
    location: Dict[str, float]
    drone_id: str
    description: Optional[str] = None

class AlertResponse(BaseModel):
    alert_id: str
    actions: List[str]
    response: int = 1

class AlertImageUpdate(BaseModel):
    alert_id: str
    image_url: str
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