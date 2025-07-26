#!/usr/bin/env python3
"""
Simple Data Viewer for Drone Alert System
"""

import requests
import json
import time
from datetime import datetime

class DataViewer:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def test_local_server(self):
        """Test if local server is running"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Local server is running!")
                return True
            else:
                print(f"❌ Local server returned status: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ Local server is not running. Start it with: python railway_minimal.py")
            return False
        except Exception as e:
            print(f"❌ Error connecting to local server: {e}")
            return False
    
    def get_alerts(self):
        """Get all alerts"""
        try:
            response = self.session.get(f"{self.base_url}/api/alerts")
            if response.status_code == 200:
                data = response.json()
                print("\n📊 Current Alerts:")
                print("=" * 40)
                if data.get("alerts"):
                    for alert in data["alerts"]:
                        print(f"Alert ID: {alert.get('alert_id', 'N/A')}")
                        print(f"Type: {alert.get('alert_type', 'N/A')}")
                        print(f"Score: {alert.get('score', 'N/A')}")
                        print(f"Drone ID: {alert.get('drone_id', 'N/A')}")
                        print(f"Timestamp: {alert.get('timestamp', 'N/A')}")
                        print(f"Response: {alert.get('response', 'N/A')}")
                        print(f"Image Received: {alert.get('image_received', 'N/A')}")
                        print("-" * 30)
                else:
                    print("No alerts found.")
                    print(f"Message: {data.get('message', 'No message')}")
            else:
                print(f"❌ Error getting alerts: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def create_test_alert(self):
        """Create a test alert"""
        test_alert = {
            "alert_type": "test_alert",
            "score": 0.85,
            "location": "test_location",
            "drone_id": "test_drone_001"
        }
        
        try:
            response = self.session.post(f"{self.base_url}/api/alerts", json=test_alert)
            if response.status_code == 200:
                data = response.json()
                print(f"\n✅ Test alert created!")
                print(f"Alert ID: {data.get('alert_id', 'N/A')}")
                print(f"Message: {data.get('message', 'N/A')}")
            else:
                print(f"❌ Error creating alert: {response.status_code}")
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def get_stats(self):
        """Get system stats"""
        try:
            response = self.session.get(f"{self.base_url}/api/stats")
            if response.status_code == 200:
                data = response.json()
                print("\n📈 System Stats:")
                print("=" * 30)
                for key, value in data.items():
                    print(f"{key}: {value}")
            else:
                print(f"❌ Error getting stats: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def test_all_endpoints(self):
        """Test all available endpoints"""
        endpoints = [
            ("Health", "/health", "GET"),
            ("Root", "/", "GET"),
            ("Get Alerts", "/api/alerts", "GET"),
            ("Stats", "/api/stats", "GET")
        ]
        
        print(f"\n🌐 Testing all endpoints on: {self.base_url}")
        print("=" * 50)
        
        for name, endpoint, method in endpoints:
            try:
                if method == "GET":
                    response = self.session.get(f"{self.base_url}{endpoint}")
                else:
                    response = self.session.post(f"{self.base_url}{endpoint}")
                
                print(f"✅ {name}: {response.status_code}")
                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(f"   Response: {json.dumps(data, indent=2)}")
                    except:
                        print(f"   Response: {response.text[:100]}...")
                else:
                    print(f"   Error: {response.text}")
            except Exception as e:
                print(f"❌ {name}: Error - {e}")
            print()

def main():
    print("📊 Drone Alert System - Data Viewer")
    print("=" * 40)
    
    # Ask for server URL
    server_url = input("Enter server URL (default: http://localhost:8000): ").strip()
    if not server_url:
        server_url = "http://localhost:8000"
    
    viewer = DataViewer(server_url)
    
    while True:
        print("\n🔍 What would you like to do?")
        print("1. Test local server")
        print("2. View all alerts")
        print("3. Create test alert")
        print("4. View system stats")
        print("5. Test all endpoints")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            viewer.test_local_server()
        elif choice == "2":
            viewer.get_alerts()
        elif choice == "3":
            viewer.create_test_alert()
        elif choice == "4":
            viewer.get_stats()
        elif choice == "5":
            viewer.test_all_endpoints()
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-6.")

if __name__ == "__main__":
    main() 