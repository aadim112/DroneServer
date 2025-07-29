#!/usr/bin/env python3
"""
Test script for Data Processing Flow
This script demonstrates the complete flow:
1. Application sends data to server
2. Server forwards to drone
3. Drone processes data and sends back
4. Application receives updated data
"""

import asyncio
import json
import websockets
import requests
import time
from datetime import datetime
from typing import Dict, Any

# Configuration
SERVER_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000"

class DataProcessingFlowTest:
    def __init__(self):
        self.app_id = "TestApp001"
        self.drone_id = "TestDrone001"
        self.received_results = []
        self.received_status_updates = []
        
    async def test_rest_api_flow(self):
        """Test the complete flow using REST API"""
        print("=== Testing REST API Data Processing Flow ===")
        
        # 1. Application creates a processing task
        print("\n1. Application creating processing task...")
        task_data = {
            "app_id": self.app_id,
            "drone_id": self.drone_id,
            "task_type": "image_analysis",
            "input_data": {
                "image_url": "https://example.com/test-image.jpg",
                "analysis_type": "object_detection",
                "parameters": {
                    "confidence_threshold": 0.8,
                    "max_objects": 10
                }
            },
            "priority": 3
        }
        
        response = requests.post(f"{SERVER_URL}/api/processing-tasks", json=task_data)
        if response.status_code == 200:
            result = response.json()
            task_id = result["task_id"]
            print(f"✅ Processing task created with ID: {task_id}")
        else:
            print(f"❌ Failed to create processing task: {response.status_code} - {response.text}")
            return
        
        # 2. Check pending tasks for drone
        print(f"\n2. Checking pending tasks for drone {self.drone_id}...")
        response = requests.get(f"{SERVER_URL}/api/processing-tasks/drone/{self.drone_id}/pending")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Found {result['count']} pending tasks for drone")
            for task in result['tasks']:
                print(f"   - Task ID: {task.get('task_id', 'N/A')}")
                print(f"   - Type: {task.get('task_type', 'N/A')}")
                print(f"   - Status: {task.get('status', 'N/A')}")
        else:
            print(f"❌ Failed to get pending tasks: {response.status_code} - {response.text}")
        
        # 3. Simulate drone processing (in real scenario, drone would process and send result)
        print(f"\n3. Simulating drone processing result...")
        result_data = {
            "task_id": task_id,
            "drone_id": self.drone_id,
            "result_data": {
                "detected_objects": [
                    {"type": "person", "confidence": 0.95, "bbox": [100, 200, 150, 300]},
                    {"type": "vehicle", "confidence": 0.87, "bbox": [300, 150, 400, 200]}
                ],
                "processing_metadata": {
                    "processing_time_ms": 1250,
                    "image_resolution": "1920x1080",
                    "algorithm_version": "v2.1"
                }
            },
            "processing_time": 1.25,
            "success": True,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # In real scenario, this would be sent via WebSocket from drone
        # For testing, we'll simulate it by directly creating the result
        try:
            # This would normally be done via WebSocket, but for testing we'll simulate
            print("   (Simulating drone sending result via WebSocket)")
            print(f"   - Task ID: {task_id}")
            print(f"   - Detected objects: {len(result_data['result_data']['detected_objects'])}")
            print(f"   - Processing time: {result_data['processing_time']}s")
        except Exception as e:
            print(f"❌ Error simulating drone processing: {e}")
        
        # 4. Check processing result
        print(f"\n4. Checking processing result...")
        response = requests.get(f"{SERVER_URL}/api/processing-results/{task_id}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Processing result found:")
            print(f"   - Task ID: {result.get('task_id', 'N/A')}")
            print(f"   - Success: {result.get('success', 'N/A')}")
            print(f"   - Processing time: {result.get('processing_time', 'N/A')}s")
        else:
            print(f"❌ Failed to get processing result: {response.status_code} - {response.text}")
        
        # 5. Check results by drone
        print(f"\n5. Checking all results for drone {self.drone_id}...")
        response = requests.get(f"{SERVER_URL}/api/processing-results/drone/{self.drone_id}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Found {result['count']} results for drone")
        else:
            print(f"❌ Failed to get results by drone: {response.status_code} - {response.text}")

    async def test_websocket_flow(self):
        """Test the complete flow using WebSocket"""
        print("\n=== Testing WebSocket Data Processing Flow ===")
        
        # Start application WebSocket connection
        print("\n1. Starting application WebSocket connection...")
        app_websocket = await websockets.connect(f"{WS_URL}/ws/application/{self.app_id}")
        
        # Wait for connection message
        welcome_msg = await app_websocket.recv()
        welcome_data = json.loads(welcome_msg)
        print(f"✅ Application connected: {welcome_data.get('client_id', 'N/A')}")
        
        # Start drone WebSocket connection
        print("\n2. Starting drone WebSocket connection...")
        drone_websocket = await websockets.connect(f"{WS_URL}/ws/drone/{self.drone_id}")
        
        # Wait for connection message
        welcome_msg = await drone_websocket.recv()
        welcome_data = json.loads(welcome_msg)
        print(f"✅ Drone connected: {welcome_data.get('client_id', 'N/A')}")
        
        # 3. Application sends processing task
        print("\n3. Application sending processing task...")
        task_data = {
            "app_id": self.app_id,
            "drone_id": self.drone_id,
            "task_type": "object_detection",
            "input_data": {
                "image_data": "base64_encoded_image_data",
                "detection_parameters": {
                    "min_confidence": 0.7,
                    "max_objects": 5
                }
            },
            "priority": 2
        }
        
        task_message = {
            "type": "processing_task",
            "data": task_data
        }
        
        await app_websocket.send(json.dumps(task_message))
        print("✅ Processing task sent from application")
        
        # 4. Wait for drone to receive task
        print("\n4. Waiting for drone to receive task...")
        try:
            drone_msg = await asyncio.wait_for(drone_websocket.recv(), timeout=5.0)
            drone_data = json.loads(drone_msg)
            if drone_data.get('type') == 'processing_task':
                task_id = drone_data.get('task_id')
                print(f"✅ Drone received processing task: {task_id}")
                
                # 5. Simulate drone processing and sending result
                print("\n5. Simulating drone processing and sending result...")
                await asyncio.sleep(2)  # Simulate processing time
                
                result_data = {
                    "task_id": task_id,
                    "drone_id": self.drone_id,
                    "result_data": {
                        "detections": [
                            {"class": "person", "confidence": 0.92, "bbox": [50, 100, 200, 400]},
                            {"class": "car", "confidence": 0.85, "bbox": [300, 200, 500, 300]}
                        ],
                        "processing_info": {
                            "algorithm": "YOLOv5",
                            "processing_time_ms": 850,
                            "image_size": "640x480"
                        }
                    },
                    "processing_time": 0.85,
                    "success": True,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
                result_message = {
                    "type": "processing_result",
                    "data": result_data
                }
                
                await drone_websocket.send(json.dumps(result_message))
                print("✅ Drone sent processing result")
                
                # 6. Wait for application to receive result
                print("\n6. Waiting for application to receive result...")
                try:
                    app_msg = await asyncio.wait_for(app_websocket.recv(), timeout=5.0)
                    app_data = json.loads(app_msg)
                    if app_data.get('type') == 'processing_result_received':
                        print(f"✅ Application received processing result:")
                        print(f"   - Task ID: {app_data.get('task_id', 'N/A')}")
                        print(f"   - Result ID: {app_data.get('result_id', 'N/A')}")
                        print(f"   - Drone ID: {app_data.get('drone_id', 'N/A')}")
                        
                        result_data = app_data.get('result_data', {})
                        detections = result_data.get('result_data', {}).get('detections', [])
                        print(f"   - Detections: {len(detections)} objects")
                    else:
                        print(f"   Received message: {app_data.get('type', 'unknown')}")
                except asyncio.TimeoutError:
                    print("   ⏰ Timeout waiting for application to receive result")
                    
            else:
                print(f"   Received unexpected message: {drone_data.get('type', 'unknown')}")
                
        except asyncio.TimeoutError:
            print("   ⏰ Timeout waiting for drone to receive task")
        
        # Close connections
        await app_websocket.close()
        await drone_websocket.close()
        print("\n✅ WebSocket connections closed")

    async def test_status_updates(self):
        """Test task status updates"""
        print("\n=== Testing Task Status Updates ===")
        
        # Start connections
        app_websocket = await websockets.connect(f"{WS_URL}/ws/application/{self.app_id}")
        drone_websocket = await websockets.connect(f"{WS_URL}/ws/drone/{self.drone_id}")
        
        # Wait for connections
        await app_websocket.recv()
        await drone_websocket.recv()
        
        # Send task
        task_data = {
            "app_id": self.app_id,
            "drone_id": self.drone_id,
            "task_type": "image_processing",
            "input_data": {"test": "data"},
            "priority": 1
        }
        
        task_message = {
            "type": "processing_task",
            "data": task_data
        }
        
        await app_websocket.send(json.dumps(task_message))
        print("✅ Task sent")
        
        # Wait for drone to receive task
        drone_msg = await asyncio.wait_for(drone_websocket.recv(), timeout=5.0)
        drone_data = json.loads(drone_msg)
        
        if drone_data.get('type') == 'processing_task':
            task_id = drone_data.get('task_id')
            
            # Simulate status updates
            status_updates = [
                {"status": "processing", "additional_data": {"progress": 25}},
                {"status": "processing", "additional_data": {"progress": 50}},
                {"status": "processing", "additional_data": {"progress": 75}},
                {"status": "completed", "additional_data": {"final_progress": 100}}
            ]
            
            for update in status_updates:
                status_message = {
                    "type": "task_status_update",
                    "data": {
                        "task_id": task_id,
                        "status": update["status"],
                        "additional_data": update["additional_data"]
                    }
                }
                
                await drone_websocket.send(json.dumps(status_message))
                print(f"✅ Status update sent: {update['status']} - {update['additional_data']}")
                await asyncio.sleep(1)
        
        await app_websocket.close()
        await drone_websocket.close()

async def main():
    """Main test function"""
    print("🔄 Data Processing Flow Test")
    print("=" * 60)
    
    test = DataProcessingFlowTest()
    
    # Test REST API flow
    await test.test_rest_api_flow()
    
    # Test WebSocket flow
    await test.test_websocket_flow()
    
    # Test status updates
    await test.test_status_updates()
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("Note: Some tests may fail if server is not running")
    print("Run 'python main.py' to start the server")

if __name__ == "__main__":
    asyncio.run(main()) 