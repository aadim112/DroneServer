import asyncio
import websockets
import json
from datetime import datetime

async def debug_alert_flow():
    """Debug the alert flow to see what's happening"""
    uri = "wss://web-production-190fc.up.railway.app/ws/drone/drone_001"
    
    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket server")
        
        # Send the same alert as websockettest.py
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
        
        print("Sending alert:", json.dumps(alert, indent=2))
        await websocket.send(json.dumps(alert))
        print("Alert sent!")
        
        # Wait a bit to see if we get any response
        try:
            response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            print("Received response:", response)
        except asyncio.TimeoutError:
            print("No response received within 5 seconds")
        except Exception as e:
            print(f"Error receiving response: {e}")

if __name__ == "__main__":
    asyncio.run(debug_alert_flow()) 