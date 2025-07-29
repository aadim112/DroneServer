#!/usr/bin/env python3
"""
Test script for Alert Image functionality
This script demonstrates how to use the new alertImage collection and endpoints.
"""

import asyncio
import json
import base64
import websockets
import requests
from datetime import datetime
from typing import Dict, Any

# Configuration
SERVER_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000"

def create_test_image_blob() -> str:
    """Create a test image blob (base64 encoded)"""
    # Create a simple test image data (1x1 pixel PNG)
    test_image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf5\xd7\xd4\xf7\x00\x00\x00\x00IEND\xaeB`\x82'
    return base64.b64encode(test_image_data).decode('utf-8')

def test_rest_api():
    """Test REST API endpoints for alert images"""
    print("=== Testing REST API Endpoints ===")
    
    # Test data
    test_alert_image = {
        "found": 1,
        "name": "Person Detected",
        "drone_id": "TestDrone001",
        "actual_image": create_test_image_blob(),
        "matched_frame": create_test_image_blob(),
        "location": [10.5, 20.3, 5.0],
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # 1. Create alert image
    print("\n1. Creating alert image...")
    response = requests.post(f"{SERVER_URL}/api/alert-images", json=test_alert_image)
    if response.status_code == 200:
        result = response.json()
        alert_image_id = result["alert_image_id"]
        print(f"✅ Alert image created with ID: {alert_image_id}")
    else:
        print(f"❌ Failed to create alert image: {response.status_code} - {response.text}")
        return
    
    # 2. Get all alert images
    print("\n2. Getting all alert images...")
    response = requests.get(f"{SERVER_URL}/api/alert-images")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Found {result['count']} alert images")
        for img in result['alert_images'][:3]:  # Show first 3
            print(f"   - ID: {img.get('id', 'N/A')}, Name: {img.get('name', 'N/A')}, Drone: {img.get('drone_id', 'N/A')}")
    else:
        print(f"❌ Failed to get alert images: {response.status_code} - {response.text}")
    
    # 3. Get specific alert image
    print(f"\n3. Getting specific alert image {alert_image_id}...")
    response = requests.get(f"{SERVER_URL}/api/alert-images/{alert_image_id}")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Alert image details:")
        print(f"   - Name: {result.get('name', 'N/A')}")
        print(f"   - Drone ID: {result.get('drone_id', 'N/A')}")
        print(f"   - Location: {result.get('location', 'N/A')}")
        print(f"   - Found: {result.get('found', 'N/A')}")
    else:
        print(f"❌ Failed to get alert image: {response.status_code} - {response.text}")
    
    # 4. Get alert images by drone
    print(f"\n4. Getting alert images by drone TestDrone001...")
    response = requests.get(f"{SERVER_URL}/api/alert-images/drone/TestDrone001")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Found {result['count']} alert images for drone {result['drone_id']}")
    else:
        print(f"❌ Failed to get alert images by drone: {response.status_code} - {response.text}")
    
    # 5. Delete alert image
    print(f"\n5. Deleting alert image {alert_image_id}...")
    response = requests.delete(f"{SERVER_URL}/api/alert-images/{alert_image_id}")
    if response.status_code == 200:
        print("✅ Alert image deleted successfully")
    else:
        print(f"❌ Failed to delete alert image: {response.status_code} - {response.text}")

async def test_websocket():
    """Test WebSocket functionality for alert images"""
    print("\n=== Testing WebSocket Endpoints ===")
    
    # Test data
    test_alert_image_data = {
        "found": 1,
        "name": "Vehicle Detected",
        "drone_id": "TestDrone002",
        "actual_image": create_test_image_blob(),
        "matched_frame": create_test_image_blob(),
        "location": [15.2, 30.1, 8.5],
        "timestamp": datetime.utcnow().isoformat()
    }
    
    try:
        # Connect as a drone
        print("\n1. Connecting as drone...")
        async with websockets.connect(f"{WS_URL}/ws/drone/TestDrone002") as websocket:
            # Wait for connection message
            welcome_msg = await websocket.recv()
            welcome_data = json.loads(welcome_msg)
            print(f"✅ Connected as drone: {welcome_data.get('client_id', 'N/A')}")
            
            # Send alert image message
            print("\n2. Sending alert image via WebSocket...")
            alert_image_message = {
                "type": "alert_image",
                "data": test_alert_image_data
            }
            await websocket.send(json.dumps(alert_image_message))
            print("✅ Alert image message sent")
            
            # Wait a bit for processing
            await asyncio.sleep(2)
            
    except Exception as e:
        print(f"❌ WebSocket test failed: {e}")

async def test_application_websocket():
    """Test application WebSocket to receive alert image notifications"""
    print("\n=== Testing Application WebSocket ===")
    
    try:
        # Connect as an application
        print("\n1. Connecting as application...")
        async with websockets.connect(f"{WS_URL}/ws/application/TestApp001") as websocket:
            # Wait for connection message
            welcome_msg = await websocket.recv()
            welcome_data = json.loads(welcome_msg)
            print(f"✅ Connected as application: {welcome_data.get('client_id', 'N/A')}")
            
            # Wait for alert image notifications
            print("\n2. Waiting for alert image notifications...")
            print("   (You can run the drone WebSocket test in another terminal to see notifications)")
            
            # Wait for up to 30 seconds for messages
            timeout = 30
            start_time = asyncio.get_event_loop().time()
            
            while (asyncio.get_event_loop().time() - start_time) < timeout:
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    data = json.loads(message)
                    
                    if data.get('type') == 'alert_image_received':
                        print(f"✅ Received alert image notification:")
                        print(f"   - Alert Image ID: {data.get('alert_image_id', 'N/A')}")
                        print(f"   - Drone ID: {data.get('drone_id', 'N/A')}")
                        print(f"   - Name: {data.get('alert_image', {}).get('name', 'N/A')}")
                        break
                    elif data.get('type') == 'pong':
                        print("   Received pong message")
                    else:
                        print(f"   Received message: {data.get('type', 'unknown')}")
                        
                except asyncio.TimeoutError:
                    continue
                except Exception as e:
                    print(f"   Error receiving message: {e}")
                    break
            
            print("   Application WebSocket test completed")
            
    except Exception as e:
        print(f"❌ Application WebSocket test failed: {e}")

def main():
    """Main test function"""
    print("🚁 Alert Image Functionality Test")
    print("=" * 50)
    
    # Test REST API endpoints
    test_rest_api()
    
    # Test WebSocket functionality
    print("\n" + "=" * 50)
    print("Note: WebSocket tests require the server to be running")
    print("Run 'python main.py' in another terminal to start the server")
    print("=" * 50)
    
    # Uncomment the following lines to test WebSocket functionality
    # (requires server to be running)
    # asyncio.run(test_websocket())
    # asyncio.run(test_application_websocket())

if __name__ == "__main__":
    main() 