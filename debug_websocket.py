#!/usr/bin/env python3
"""
Debug WebSocket Alert Functionality
"""

import asyncio
import websockets
import json
from datetime import datetime

async def test_websocket_alert():
    """Test sending an alert via WebSocket"""
    
    # Connect to the WebSocket server
    uri = "ws://localhost:8000/ws/drone/test_drone_001"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to WebSocket server")
            
            # Wait for connection message
            connection_msg = await websocket.recv()
            print(f"📨 Connection message: {connection_msg}")
            
            # Send a test alert
            test_alert = {
                "type": "alert",
                "data": {
                    "alert_type": "intrusion",
                    "score": 0.85,
                    "location": {"lat": 40.7128, "lng": -74.0060},
                    "drone_id": "test_drone_001",
                    "description": "Test intrusion alert via WebSocket",
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
            
            print(f"📤 Sending alert: {json.dumps(test_alert, indent=2)}")
            await websocket.send(json.dumps(test_alert))
            
            # Wait a moment for processing
            await asyncio.sleep(2)
            
            print("✅ Alert sent successfully")
            
    except Exception as e:
        print(f"❌ Error: {e}")

async def test_rest_api():
    """Test REST API to see current alerts"""
    import aiohttp
    
    try:
        async with aiohttp.ClientSession() as session:
            # Get all alerts
            async with session.get("http://localhost:8000/api/alerts") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"📊 Current alerts in database: {data['count']}")
                    for alert in data['alerts']:
                        print(f"  - {alert['alert_id']}: {alert['alert_type']} (score: {alert['score']})")
                else:
                    print(f"❌ Failed to get alerts: {response.status}")
    except Exception as e:
        print(f"❌ REST API error: {e}")

async def main():
    """Main test function"""
    print("🔍 Debugging WebSocket Alert Functionality")
    print("=" * 50)
    
    # First check current alerts
    print("\n1. Checking current alerts in database...")
    await test_rest_api()
    
    # Test WebSocket alert
    print("\n2. Testing WebSocket alert...")
    await test_websocket_alert()
    
    # Check alerts again
    print("\n3. Checking alerts after WebSocket test...")
    await asyncio.sleep(3)  # Wait for processing
    await test_rest_api()
    
    print("\n✅ Debug test completed")

if __name__ == "__main__":
    asyncio.run(main()) 