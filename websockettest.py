import asyncio
import websockets
from datetime import datetime
import json

async def send_alert():
    uri = "wss://web-production-190fc.up.railway.app/ws/drone/drone_001"
    async with websockets.connect(uri) as websocket:
        alert = {
            "type": "alert",
            "data": {
                "alert": "abc!",
                "alert_location": [0.0, 0.0, 0.0],
                "timestamp": datetime.now().isoformat(),
                "alert_type": "Crowd",
                "score": 98.5,
                "drone_id": "drone_001"
            }
        }
        await websocket.send(json.dumps(alert))
        print("Alert sent!", alert)

asyncio.run(send_alert())