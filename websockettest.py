import asyncio
import websockets
import json

async def send_alert():
    uri = "wss://web-production-190fc.up.railway.app/ws/drone/drone_001"
    async with websockets.connect(uri) as websocket:
        alert = {
            "type": "alert",
            "data": {
                "alert": "Hela 2 Detected",
                "alert_location": [0.0, 0.0, 0.0],
                "timestamp": "2025-07-28T12:16:07.965060",
                "alert_type": "flood",
                "score": 98.5,
                "drone_id": "drone_001"
            }
        }
        await websocket.send(json.dumps(alert))
        print("Alert sent!")

asyncio.run(send_alert())