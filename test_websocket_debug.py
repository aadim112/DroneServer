#!/usr/bin/env python3
"""
Debug WebSocket Connection
Simple script to test WebSocket connection and see what's happening
"""

import asyncio
import json
import websockets
import os
from datetime import datetime

# Configuration
WS_URL = "wss://web-production-190fc.up.railway.app"
APP_ID = "debug_app_001"

async def test_websocket_connection():
    """Test WebSocket connection and send a simple message"""
    
    print("🔍 WebSocket Debug Test")
    print("=" * 50)
    
    try:
        # Connect to WebSocket
        uri = f"{WS_URL}/ws/application/{APP_ID}"
        print(f"🔌 Connecting to: {uri}")
        
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to WebSocket server")
            
            # Wait for welcome message
            try:
                welcome_msg = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                welcome_data = json.loads(welcome_msg)
                print(f"📨 Received welcome message: {welcome_data}")
            except asyncio.TimeoutError:
                print("⚠️  No welcome message received (timeout)")
            except Exception as e:
                print(f"⚠️  Error receiving welcome message: {e}")
            
            # Send a simple test message
            test_message = {
                "type": "ping",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            print(f"📤 Sending test message: {test_message}")
            await websocket.send(json.dumps(test_message))
            
            # Wait for response
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                response_data = json.loads(response)
                print(f"📨 Received response: {response_data}")
            except asyncio.TimeoutError:
                print("⚠️  No response received (timeout)")
            except Exception as e:
                print(f"⚠️  Error receiving response: {e}")
            
            # Test alert image message
            test_alert_data = {
                "found": 1,
                "name": "Test Object",
                "drone_id": "TestDrone001",
                "actual_image": "dGVzdF9pbWFnZV9kYXRh",  # base64 encoded "test_image_data"
                "matched_frame": "dGVzdF9mcmFtZV9kYXRh",  # base64 encoded "test_frame_data"
                "location": [10.0, 20.0, 5.0],
                "timestamp": datetime.utcnow().isoformat()
            }
            
            alert_message = {
                "type": "alert_image",
                "data": test_alert_data
            }
            
            print(f"📤 Sending alert image message: {alert_message}")
            await websocket.send(json.dumps(alert_message))
            
            # Wait for alert image response
            try:
                alert_response = await asyncio.wait_for(websocket.recv(), timeout=10.0)
                alert_response_data = json.loads(alert_response)
                print(f"📨 Received alert response: {alert_response_data}")
            except asyncio.TimeoutError:
                print("⚠️  No alert response received (timeout)")
            except Exception as e:
                print(f"⚠️  Error receiving alert response: {e}")
            
            print("✅ WebSocket test completed")
            
    except Exception as e:
        print(f"❌ WebSocket connection failed: {e}")
        print(f"   URL: {uri}")
        print(f"   Error type: {type(e).__name__}")

async def main():
    """Main function"""
    await test_websocket_connection()

if __name__ == "__main__":
    asyncio.run(main()) 