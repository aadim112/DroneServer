#!/usr/bin/env python3
"""
Test Deployed API - Send data to the deployed Railway server
"""

import requests
import json
import time
from datetime import datetime

class DeployedAPITester:
    def __init__(self, base_url="https://droneserver-production.up.railway.app"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def create_group(self, region="test_region", purpose="surveillance", rl_model_instance="test_model"):
        """Create a group"""
        try:
            url = f"{self.base_url}/api/v1/groups/create/"
            params = {
                "region": region,
                "purpose": purpose,
                "rl_model_instance": rl_model_instance
            }
            
            response = self.session.post(url, params=params, timeout=10)
            print(f"📡 Creating group...")
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ Group created successfully!")
                return True
            else:
                print(f"   ❌ Failed to create group")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"   ❌ Error creating group: {e}")
            return False
    
    def register_drone(self, drone_id=1, location="test_location", purpose="surveillance"):
        """Register a drone"""
        try:
            url = f"{self.base_url}/api/v1/drones/register/"
            params = {
                "drone_id": drone_id,
                "location": location,
                "purpose": purpose
            }
            
            response = self.session.post(url, params=params, timeout=10)
            print(f"📡 Registering drone {drone_id}...")
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ Drone registered successfully!")
                return True
            else:
                print(f"   ❌ Failed to register drone")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"   ❌ Error registering drone: {e}")
            return False
    
    def upload_data(self, drone_id=1, location="test_location", score=0.85, casuality="test_alert"):
        """Upload data from drone"""
        try:
            url = f"{self.base_url}/api/v1/drones/data/"
            
            # Create a simple test image (base64 encoded small image)
            test_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
            
            data = {
                "drone_id": drone_id,
                "location": location,
                "score": score,
                "casuality": casuality
            }
            
            files = {
                "image": ("test_image.jpg", test_image, "image/jpeg")
            }
            
            response = self.session.post(url, data=data, files=files, timeout=10)
            print(f"📡 Uploading data from drone {drone_id}...")
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ Data uploaded successfully!")
                return True
            else:
                print(f"   ❌ Failed to upload data")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"   ❌ Error uploading data: {e}")
            return False
    
    def get_data_logs(self, drone_id=None, limit=10):
        """Get data logs"""
        try:
            url = f"{self.base_url}/api/v1/drones/data/"
            params = {"limit": limit}
            if drone_id:
                params["drone_id"] = drone_id
            
            response = self.session.get(url, params=params, timeout=10)
            print(f"📡 Getting data logs...")
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Data logs retrieved!")
                print(f"   Count: {len(data) if isinstance(data, list) else 'N/A'}")
                return data
            else:
                print(f"   ❌ Failed to get data logs")
                print(f"   Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error getting data logs: {e}")
            return None
    
    def send_control(self, group_id=1, command="test_command"):
        """Send control command"""
        try:
            url = f"{self.base_url}/api/v1/drones/control/"
            params = {
                "group_id": group_id,
                "command": command
            }
            
            response = self.session.post(url, params=params, timeout=10)
            print(f"📡 Sending control command...")
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ Control command sent successfully!")
                return True
            else:
                print(f"   ❌ Failed to send control command")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"   ❌ Error sending control command: {e}")
            return False

def main():
    """Main test function"""
    print("🚁 Testing Deployed Drone API")
    print("=" * 50)
    
    # Initialize tester
    tester = DeployedAPITester()
    
    # Test 1: Create a group
    print("\n1. Creating a test group...")
    group_created = tester.create_group(
        region="New York",
        purpose="surveillance",
        rl_model_instance="drone_surveillance_v1"
    )
    
    # Test 2: Register a drone
    print("\n2. Registering a test drone...")
    drone_registered = tester.register_drone(
        drone_id=1,
        location="40.7128,-74.0060",
        purpose="surveillance"
    )
    
    # Test 3: Upload data from drone
    print("\n3. Uploading test data...")
    data_uploaded = tester.upload_data(
        drone_id=1,
        location="40.7128,-74.0060",
        score=0.95,
        casuality="intrusion_detected"
    )
    
    # Test 4: Get data logs
    print("\n4. Getting data logs...")
    logs = tester.get_data_logs(drone_id=1, limit=5)
    
    # Test 5: Send control command
    print("\n5. Sending control command...")
    control_sent = tester.send_control(
        group_id=1,
        command="move_to_location"
    )
    
    # Test 6: Upload more data with different scenarios
    print("\n6. Uploading multiple test scenarios...")
    test_scenarios = [
        {"drone_id": 1, "location": "40.7589,-73.9851", "score": 0.88, "casuality": "fire_detected"},
        {"drone_id": 1, "location": "40.7505,-73.9934", "score": 0.76, "casuality": "object_detected"},
        {"drone_id": 1, "location": "40.7484,-73.9857", "score": 0.82, "casuality": "motion_detected"},
        {"drone_id": 1, "location": "40.7527,-73.9772", "score": 0.45, "casuality": "suspicious_activity"}
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"   Uploading scenario {i}: {scenario['casuality']}")
        tester.upload_data(**scenario)
        time.sleep(1)
    
    # Test 7: Get final data logs
    print("\n7. Getting final data logs...")
    final_logs = tester.get_data_logs(limit=10)
    
    print("\n✅ API Testing Completed!")
    print(f"   Group created: {'✅' if group_created else '❌'}")
    print(f"   Drone registered: {'✅' if drone_registered else '❌'}")
    print(f"   Data uploaded: {'✅' if data_uploaded else '❌'}")
    print(f"   Control sent: {'✅' if control_sent else '❌'}")
    
    print(f"\n🌐 API Documentation:")
    print(f"   Docs: {tester.base_url}/docs")
    print(f"   OpenAPI: {tester.base_url}/openapi.json")

if __name__ == "__main__":
    main() 