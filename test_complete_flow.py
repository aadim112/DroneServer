import asyncio
import websockets
import json
from datetime import datetime
import time

async def test_complete_flow():
    """Test the complete flow from drone sending alert to application receiving it"""
    
    # First, connect as an application to listen for alerts
    app_uri = "wss://web-production-190fc.up.railway.app/ws/application/test_app_001"
    drone_uri = "wss://web-production-190fc.up.railway.app/ws/drone/drone_001"
    
    print("Starting complete flow test...")
    
    # Connect as application first
    async with websockets.connect(app_uri) as app_websocket:
        print("✅ Application connected")
        
        # Wait for connection message
        try:
            app_msg = await asyncio.wait_for(app_websocket.recv(), timeout=5.0)
            app_data = json.loads(app_msg)
            print(f"📨 Application received: {app_data.get('type')}")
        except asyncio.TimeoutError:
            print("⚠️ No initial message received by application")
        
        # Now connect as drone and send alert
        async with websockets.connect(drone_uri) as drone_websocket:
            print("✅ Drone connected")
            
            # Wait for drone connection message
            try:
                drone_msg = await asyncio.wait_for(drone_websocket.recv(), timeout=5.0)
                drone_data = json.loads(drone_msg)
                print(f"📨 Drone received: {drone_data.get('type')}")
            except asyncio.TimeoutError:
                print("⚠️ No initial message received by drone")
            
            # Send alert from drone
            alert = {
                "type": "alert",
                "data": {
                    "alert": "Test Alert from Complete Flow",
                    "alert_location": [10.0, 20.0, 5.0],
                    "timestamp": datetime.now().isoformat(),
                    "alert_type": "test",
                    "score": 95.5,
                    "drone_id": "drone_001"
                }
            }
            
            print(f"📤 Sending alert: {json.dumps(alert, indent=2)}")
            await drone_websocket.send(json.dumps(alert))
            print("✅ Alert sent from drone")
            
            # Wait for application to receive the alert
            try:
                app_alert_msg = await asyncio.wait_for(app_websocket.recv(), timeout=10.0)
                app_alert_data = json.loads(app_alert_msg)
                print(f"📨 Application received alert: {app_alert_data.get('type')}")
                print(f"📋 Alert data: {json.dumps(app_alert_data, indent=2)}")
                
                if app_alert_data.get('type') == 'new_alert':
                    print("🎉 SUCCESS: Application received the alert!")
                    alert_data = app_alert_data.get('alert', {})
                    print(f"Alert message: {alert_data.get('alert')}")
                    print(f"Alert ID: {app_alert_data.get('alert_id')}")
                else:
                    print(f"❌ Unexpected message type: {app_alert_data.get('type')}")
                    
            except asyncio.TimeoutError:
                print("❌ FAILED: Application did not receive alert within 10 seconds")
            
            # Wait a bit more to see if there are any additional messages
            try:
                additional_msg = await asyncio.wait_for(app_websocket.recv(), timeout=3.0)
                additional_data = json.loads(additional_msg)
                print(f"📨 Additional message: {additional_data.get('type')}")
            except asyncio.TimeoutError:
                print("ℹ️ No additional messages")
    
    print("🏁 Test completed")

if __name__ == "__main__":
    asyncio.run(test_complete_flow()) 