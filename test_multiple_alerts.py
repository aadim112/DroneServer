import asyncio
import websockets
import json
import time
from datetime import datetime

async def send_multiple_alerts():
    """Send multiple alerts to test the serialization fix"""
    uri = "wss://web-production-190fc.up.railway.app/ws/drone/drone_001"
    
    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket server")
        
        # Send multiple alerts with different data
        alerts = [
            {
                "type": "alert",
                "data": {
                    "alert": "Flood Detection Alert 1",
                    "alert_location": [10.0, 20.0, 5.0],
                    "timestamp": datetime.utcnow().isoformat(),
                    "alert_type": "flood",
                    "score": 95.5,
                    "drone_id": "drone_001"
                }
            },
            {
                "type": "alert", 
                "data": {
                    "alert": "Casualty Detection Alert 2",
                    "alert_location": [15.0, 25.0, 8.0],
                    "timestamp": datetime.utcnow().isoformat(),
                    "alert_type": "casualty",
                    "score": 87.3,
                    "drone_id": "drone_001"
                }
            },
            {
                "type": "alert",
                "data": {
                    "alert": "Fire Detection Alert 3", 
                    "alert_location": [30.0, 40.0, 12.0],
                    "timestamp": datetime.utcnow().isoformat(),
                    "alert_type": "fire",
                    "score": 92.1,
                    "drone_id": "drone_001"
                }
            },
            {
                "type": "alert",
                "data": {
                    "alert": "Structural Damage Alert 4",
                    "alert_location": [45.0, 55.0, 15.0], 
                    "timestamp": datetime.utcnow().isoformat(),
                    "alert_type": "structural",
                    "score": 78.9,
                    "drone_id": "drone_001"
                }
            },
            {
                "type": "alert",
                "data": {
                    "alert": "Medical Emergency Alert 5",
                    "alert_location": [60.0, 70.0, 10.0],
                    "timestamp": datetime.utcnow().isoformat(),
                    "alert_type": "medical",
                    "score": 96.7,
                    "drone_id": "drone_001"
                }
            }
        ]
        
        for i, alert in enumerate(alerts, 1):
            try:
                await websocket.send(json.dumps(alert))
                print(f"Alert {i} sent successfully: {alert['data']['alert']}")
                
                # Wait a bit between alerts
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f"Error sending alert {i}: {e}")
        
        print("All alerts sent! Check your application to see if all alerts are received.")

if __name__ == "__main__":
    asyncio.run(send_multiple_alerts()) 