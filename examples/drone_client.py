#!/usr/bin/env python3
"""
Example Drone Client
Simulates a drone that sends alerts and receives commands via WebSocket
"""

import asyncio
import websockets
import json
import uuid
import time
from datetime import datetime
from typing import Dict, Any

class DroneClient:
    def __init__(self, drone_id: str, server_url: str = "ws://localhost:8000"):
        self.drone_id = drone_id
        self.server_url = f"{server_url}/ws/drone/{drone_id}"
        self.websocket = None
        self.connected = False
        
    async def connect(self):
        """Connect to the WebSocket server"""
        try:
            self.websocket = await websockets.connect(self.server_url)
            self.connected = True
            print(f"Drone {self.drone_id} connected to server")
            
            # Send initial connection message
            await self.send_message({
                "type": "ping",
                "data": {"drone_id": self.drone_id}
            })
            
        except Exception as e:
            print(f"Failed to connect: {e}")
            self.connected = False
    
    async def disconnect(self):
        """Disconnect from the server"""
        if self.websocket:
            await self.websocket.close()
            self.connected = False
            print(f"Drone {self.drone_id} disconnected")
    
    async def send_message(self, message: Dict[str, Any]):
        """Send a message to the server"""
        if not self.connected or not self.websocket:
            print("Not connected to server")
            return
        
        try:
            await self.websocket.send(json.dumps(message))
        except Exception as e:
            print(f"Error sending message: {e}")
            self.connected = False
    
    async def send_alert(self, alert_type: str, score: float, location: Dict[str, float], description: str = None):
        """Send an alert to the server"""
        alert_data = {
            "type": "alert",
            "data": {
                "alert_type": alert_type,
                "score": score,
                "location": location,
                "drone_id": self.drone_id,
                "description": description,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
        
        await self.send_message(alert_data)
        print(f"Alert sent: {alert_type} at {location}")
    
    async def send_image(self, alert_id: str, image_url: str):
        """Send image data to the server"""
        image_data = {
            "type": "image",
            "data": {
                "alert_id": alert_id,
                "image_url": image_url,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
        
        await self.send_message(image_data)
        print(f"Image sent for alert {alert_id}")
    
    async def handle_command(self, command_data: Dict[str, Any]):
        """Handle commands received from the server"""
        command_type = command_data.get("type")
        alert_id = command_data.get("alert_id")
        actions = command_data.get("actions", [])
        
        print(f"Received command: {command_type}")
        print(f"Alert ID: {alert_id}")
        print(f"Actions: {actions}")
        
        # Simulate executing the command
        print("Executing drone actions...")
        await asyncio.sleep(2)  # Simulate processing time
        
        # Simulate sending back an image
        image_url = f"http://localhost:8000/uploads/drone_{self.drone_id}_alert_{alert_id}.jpg"
        await self.send_image(alert_id, image_url)
    
    async def listen_for_messages(self):
        """Listen for incoming messages from the server"""
        if not self.websocket:
            return
        
        try:
            async for message in self.websocket:
                try:
                    data = json.loads(message)
                    message_type = data.get("type")
                    
                    if message_type == "connection_established":
                        print(f"Connection established: {data}")
                    
                    elif message_type == "drone_command":
                        await self.handle_command(data)
                    
                    elif message_type == "pong":
                        print("Received pong from server")
                    
                    else:
                        print(f"Received message: {data}")
                        
                except json.JSONDecodeError:
                    print(f"Invalid JSON received: {message}")
                    
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed by server")
            self.connected = False
        except Exception as e:
            print(f"Error receiving message: {e}")
            self.connected = False
    
    async def run(self):
        """Main run loop for the drone client"""
        await self.connect()
        
        if not self.connected:
            return
        
        # Start listening for messages in background
        listen_task = asyncio.create_task(self.listen_for_messages())
        
        try:
            # Simulate periodic alerts
            alert_count = 0
            while self.connected:
                # Send a random alert every 30 seconds
                if alert_count % 6 == 0:  # Every 30 seconds (6 * 5 second sleep)
                    alert_types = ["intrusion", "fire", "accident", "security_breach", "environmental"]
                    alert_type = alert_types[alert_count % len(alert_types)]
                    
                    location = {
                        "lat": 40.7128 + (alert_count * 0.001),  # Simulate movement
                        "lng": -74.0060 + (alert_count * 0.001)
                    }
                    
                    score = 0.7 + (alert_count * 0.1) % 0.3  # Random score between 0.7-1.0
                    
                    await self.send_alert(
                        alert_type=alert_type,
                        score=score,
                        location=location,
                        description=f"Simulated {alert_type} alert #{alert_count + 1}"
                    )
                
                await asyncio.sleep(5)  # Wait 5 seconds
                alert_count += 1
                
        except KeyboardInterrupt:
            print("Shutting down drone client...")
        finally:
            listen_task.cancel()
            await self.disconnect()

async def main():
    """Main function to run the drone client"""
    drone_id = input("Enter drone ID (or press Enter for auto-generated): ").strip()
    if not drone_id:
        drone_id = f"drone_{uuid.uuid4().hex[:8]}"
    
    drone = DroneClient(drone_id)
    await drone.run()

if __name__ == "__main__":
    asyncio.run(main()) 