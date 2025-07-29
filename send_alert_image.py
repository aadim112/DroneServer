#!/usr/bin/env python3
"""
Send Alert Image to Server
Simple and clean way to send alert images from local as an application to the server.
"""

import requests
import base64
import json
import os
from datetime import datetime
from typing import Optional, Dict, Any

# Configuration
SERVER_URL = "https://web-production-190fc.up.railway.app"

class AlertImageSender:
    """Simple class to send alert images to the server"""
    
    def __init__(self, server_url: str = SERVER_URL):
        self.server_url = server_url
    
    def send_alert_image(self, 
                        actual_image_path: str,
                        matched_frame_path: str,
                        name: str = "Object Detected",
                        drone_id: str = "No Drone",
                        location: list = [0, 0, 0],
                        found: int = 1) -> Optional[str]:
        """
        Send alert image to the server
        
        Args:
            actual_image_path: Path to the actual captured image
            matched_frame_path: Path to the matched reference frame
            name: Name or description of the detected object
            drone_id: ID of the drone (or "No Drone" if not from drone)
            location: Location coordinates [x, y, z]
            found: Detection status (1=found, 0=not found)
        
        Returns:
            alert_image_id: ID of the created alert image, or None if failed
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
            
            # Send to server
            response = requests.post(
                f"{self.server_url}/api/alert-images",
                json=alert_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                alert_image_id = result.get("alert_image_id")
                print(f"✅ Alert image sent successfully!")
                print(f"   - ID: {alert_image_id}")
                print(f"   - Name: {name}")
                print(f"   - Drone: {drone_id}")
                print(f"   - Location: {location}")
                return alert_image_id
            else:
                print(f"❌ Failed to send alert image")
                print(f"   - Status Code: {response.status_code}")
                print(f"   - Response: {response.text}")
                return None
                
        except FileNotFoundError as e:
            print(f"❌ File not found: {e}")
            return None
        except Exception as e:
            print(f"❌ Error sending alert image: {e}")
            return None
    
    def send_alert_image_from_bytes(self,
                                   actual_image_bytes: bytes,
                                   matched_frame_bytes: bytes,
                                   name: str = "Object Detected",
                                   drone_id: str = "No Drone",
                                   location: list = [0, 0, 0],
                                   found: int = 1) -> Optional[str]:
        """
        Send alert image using image bytes (for OpenCV/numpy images)
        
        Args:
            actual_image_bytes: Actual image as bytes
            matched_frame_bytes: Matched frame as bytes
            name: Name or description of the detected object
            drone_id: ID of the drone
            location: Location coordinates [x, y, z]
            found: Detection status (1=found, 0=not found)
        
        Returns:
            alert_image_id: ID of the created alert image, or None if failed
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
            
            # Send to server
            response = requests.post(
                f"{self.server_url}/api/alert-images",
                json=alert_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                alert_image_id = result.get("alert_image_id")
                print(f"✅ Alert image sent successfully!")
                print(f"   - ID: {alert_image_id}")
                print(f"   - Name: {name}")
                print(f"   - Drone: {drone_id}")
                print(f"   - Location: {location}")
                return alert_image_id
            else:
                print(f"❌ Failed to send alert image")
                print(f"   - Status Code: {response.status_code}")
                print(f"   - Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error sending alert image: {e}")
            return None
    
    def get_alert_images(self, limit: int = 10) -> list:
        """Get recent alert images from the server"""
        try:
            response = requests.get(f"{self.server_url}/api/alert-images?limit={limit}")
            
            if response.status_code == 200:
                result = response.json()
                images = result.get("alert_images", [])
                print(f"✅ Found {len(images)} alert images")
                return images
            else:
                print(f"❌ Failed to get alert images: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error getting alert images: {e}")
            return []

def main():
    """Main function to demonstrate usage"""
    
    print("🚁 Alert Image Sender")
    print("=" * 40)
    
    # Initialize sender
    sender = AlertImageSender()
    
    # Example 1: Send from file paths
    print("\n1. Sending alert image from files...")
    
    # Replace these paths with your actual image files
    actual_image_path = "C:/Users/aamp8/Desktop/inno-Hackthon/Final Server/kalu2.jpg"  # Replace with your path
    matched_frame_path = "C:/Users/aamp8/Desktop/inno-Hackthon/Final Server/kalu2.jpg"  # Replace with your path
    
    if os.path.exists(actual_image_path) and os.path.exists(matched_frame_path):
        alert_id = sender.send_alert_image(
            actual_image_path=actual_image_path,
            matched_frame_path=matched_frame_path,
            name="Person Detected",
            drone_id="MyDrone001",
            location=[10.5, 20.3, 5.0],
            found=1
        )
        
        if alert_id:
            print(f"✅ Successfully sent alert image with ID: {alert_id}")
        else:
            print("❌ Failed to send alert image")
    else:
        print("⚠️  Image files not found. Please update the file paths in the script.")
        print(f"   Actual image path: {actual_image_path}")
        print(f"   Matched frame path: {matched_frame_path}")
    
    # Example 2: Get recent alert images
    print("\n2. Getting recent alert images...")
    recent_images = sender.get_alert_images(limit=5)
    
    if recent_images:
        print("Recent alert images:")
        for img in recent_images:
            print(f"  - ID: {img.get('id', 'N/A')}")
            print(f"    Name: {img.get('name', 'N/A')}")
            print(f"    Drone: {img.get('drone_id', 'N/A')}")
            print(f"    Found: {img.get('found', 'N/A')}")
            print()
    
    print("✅ Script completed!")
    print("Note: Make sure the server is running (python main.py)")

if __name__ == "__main__":
    main() 