#!/usr/bin/env python3
"""
Send Alert Image via WebSocket
Sends alert images to server via WebSocket, which then forwards to drones.
"""

import asyncio
import json
import base64
import websockets
import os
from datetime import datetime
from typing import Optional

# Configuration
WS_URL = "wss://web-production-190fc.up.railway.app"  # Change to your server WebSocket URL
SERVER_URL = "https://web-production-190fc.up.railway.app"

class WebSocketAlertImageSender:
    """Send alert images via WebSocket to server, which forwards to drones"""
    
    def __init__(self, app_id: str = "app_001"):
        self.app_id = app_id
        self.ws_url = WS_URL
        self.websocket = None
    
    async def connect(self):
        """Connect to the WebSocket server"""
        try:
            uri = f"{self.ws_url}/ws/application/{self.app_id}"
            print(f"🔌 Connecting to WebSocket: {uri}")
            self.websocket = await websockets.connect(uri)
            
            # Wait for connection message
            welcome_msg = await self.websocket.recv()
            welcome_data = json.loads(welcome_msg)
            print(f"✅ Connected as application: {welcome_data.get('client_id', 'N/A')}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to connect: {e}")
            print(f"   WebSocket URL: {uri}")
            return False
    
    async def disconnect(self):
        """Disconnect from the WebSocket server"""
        if self.websocket:
            await self.websocket.close()
            print("✅ Disconnected from WebSocket server")
    
    async def send_alert_image(self, 
                              actual_image_path: str,
                              matched_frame_path: str,
                              name: str = "Object Detected",
                              drone_id: str = "No Drone",
                              location: list = [0, 0, 0],
                              found: int = 1) -> bool:
        """
        Send alert image via WebSocket to server, which saves it and forwards to drone
        
        Args:
            actual_image_path: Path to the actual captured image
            matched_frame_path: Path to the matched reference frame
            name: Name or description of the detected object
            drone_id: ID of the drone to receive the alert
            location: Location coordinates [x, y, z]
            found: Detection status (1=found, 0=not found)
        
        Returns:
            bool: True if sent successfully, False otherwise
        """
        
        try:
            # Validate file paths
            if not os.path.exists(actual_image_path):
                raise FileNotFoundError(f"Actual image not found: {actual_image_path}")
            
            if not os.path.exists(matched_frame_path):
                raise FileNotFoundError(f"Matched frame not found: {matched_frame_path}")
            
            # Read and encode images
            with open(actual_image_path, "rb") as f:
                actual_image_blob = base64.b64encode(f.read()).decode('utf-8')
            
            with open(matched_frame_path, "rb") as f:
                matched_frame_blob = base64.b64encode(f.read()).decode('utf-8')
            
            # Create alert image data
            alert_data = {
                "found": found,
                "name": name,
                "drone_id": drone_id,
                "actual_image": actual_image_blob,
                "matched_frame": matched_frame_blob,
                "location": location,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Create WebSocket message
            message = {
                "type": "alert_image",
                "data": alert_data
            }
            
            # Send message via WebSocket
            message_json = json.dumps(message)
            print(f"📤 Sending WebSocket message: {message_json[:200]}...")
            await self.websocket.send(message_json)
            print(f"✅ Alert image sent via WebSocket to server")
            print(f"   - Name: {name}")
            print(f"   - Drone: {drone_id}")
            print(f"   - Location: {location}")
            print(f"   - Server will save and forward to drone")
            
            return True
            
        except FileNotFoundError as e:
            print(f"❌ File not found: {e}")
            return False
        except Exception as e:
            print(f"❌ Error sending alert image: {e}")
            return False
    
    async def send_alert_image_from_bytes(self,
                                         actual_image_bytes: bytes,
                                         matched_frame_bytes: bytes,
                                         name: str = "Object Detected",
                                         drone_id: str = "No Drone",
                                         location: list = [0, 0, 0],
                                         found: int = 1) -> bool:
        """
        Send alert image from memory bytes via WebSocket
        
        Args:
            actual_image_bytes: Actual image as bytes
            matched_frame_bytes: Matched frame as bytes
            name: Name or description of the detected object
            drone_id: ID of the drone to receive the alert
            location: Location coordinates [x, y, z]
            found: Detection status (1=found, 0=not found)
        
        Returns:
            bool: True if sent successfully, False otherwise
        """
        
        try:
            # Encode images to base64
            actual_image_blob = base64.b64encode(actual_image_bytes).decode('utf-8')
            matched_frame_blob = base64.b64encode(matched_frame_bytes).decode('utf-8')
            
            # Create alert image data
            alert_data = {
                "found": found,
                "name": name,
                "drone_id": drone_id,
                "actual_image": actual_image_blob,
                "matched_frame": matched_frame_blob,
                "location": location,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Create WebSocket message
            message = {
                "type": "alert_image",
                "data": alert_data
            }
            
            # Send message via WebSocket
            message_json = json.dumps(message)
            print(f"📤 Sending WebSocket message: {message_json[:200]}...")
            await self.websocket.send(message_json)
            print(f"✅ Alert image sent via WebSocket to server")
            print(f"   - Name: {name}")
            print(f"   - Drone: {drone_id}")
            print(f"   - Location: {location}")
            print(f"   - Server will save and forward to drone")
            
            return True
            
        except Exception as e:
            print(f"❌ Error sending alert image: {e}")
            return False
    
    async def listen_for_notifications(self, timeout: int = 30):
        """Listen for notifications from the server"""
        try:
            print(f"🔊 Listening for server notifications (timeout: {timeout}s)...")
            
            start_time = asyncio.get_event_loop().time()
            
            while (asyncio.get_event_loop().time() - start_time) < timeout:
                try:
                    message = await asyncio.wait_for(self.websocket.recv(), timeout=1.0)
                    data = json.loads(message)
                    
                    if data.get('type') == 'alert_image_received':
                        print(f"📨 Server confirmed alert image received:")
                        print(f"   - Alert Image ID: {data.get('alert_image_id', 'N/A')}")
                        print(f"   - Drone ID: {data.get('drone_id', 'N/A')}")
                        print(f"   - Name: {data.get('alert_image', {}).get('name', 'N/A')}")
                    elif data.get('type') == 'pong':
                        print("   Received pong message")
                    else:
                        print(f"   Received message: {data.get('type', 'unknown')}")
                        
                except asyncio.TimeoutError:
                    continue
                except Exception as e:
                    print(f"   Error receiving message: {e}")
                    break
            
            print("   Listening completed")
            
        except Exception as e:
            print(f"❌ Error listening for notifications: {e}")

async def main():
    """Main function to demonstrate WebSocket usage"""
    
    print("🚁 WebSocket Alert Image Sender")
    print("=" * 50)
    print("This sends alert images to server via WebSocket")
    print("Server will save the image and forward to drone")
    print("=" * 50)
    
    # Initialize sender
    sender = WebSocketAlertImageSender(app_id="MyApp001")
    
    # Connect to WebSocket
    if await sender.connect():
        
        # Example 1: Send from file paths
        print("\n1. Sending alert image from files via WebSocket...")
        
        # Replace these paths with your actual image files
        actual_image_path = "C:/Users/aamp8/Desktop/inno-Hackthon/Final Server/kalu2.jpg"
        matched_frame_path = "C:/Users/aamp8/Desktop/inno-Hackthon/Final Server/kalu2.jpg"
        
        if os.path.exists(actual_image_path) and os.path.exists(matched_frame_path):
            success = await sender.send_alert_image(
                actual_image_path=actual_image_path,
                matched_frame_path=matched_frame_path,
                name="Person Detected via WebSocket",
                drone_id="MyDrone001",
                location=[10.5, 20.3, 5.0],
                found=1
            )
            
            if success:
                print("✅ Successfully sent alert image via WebSocket")
                print("   Server will save the image and forward to drone")
            else:
                print("❌ Failed to send alert image via WebSocket")
        else:
            print("⚠️  Image files not found. Please update the file paths.")
            print(f"   Actual image path: {actual_image_path}")
            print(f"   Matched frame path: {matched_frame_path}")
        
        # Example 2: Listen for notifications
        print("\n2. Listening for server notifications...")
        await sender.listen_for_notifications(timeout=10)
        
        # Disconnect
        await sender.disconnect()
    
    print("\n✅ WebSocket script completed!")
    print("Note: Make sure the server is running and supports WebSocket connections")

if __name__ == "__main__":
    asyncio.run(main()) 