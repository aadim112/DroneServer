#!/usr/bin/env python3
"""
Test Local Server - Test the server locally before deployment
"""

import requests
import json
import time
from datetime import datetime

class LocalServerTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def test_server_health(self):
        """Test if server is running and healthy"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Server is running and healthy!")
                return True
            else:
                print(f"❌ Server returned status: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ Server is not running. Start it with: python main.py")
            return False
        except Exception as e:
            print(f"❌ Error connecting to server: {e}")
            return False
    
    def send_alert(self, alert_data):
        """Send alert data to the server"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/alerts",
                json=alert_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Alert sent successfully!")
                print(f"   Alert ID: {result.get('alert_id', 'N/A')}")
                print(f"   Message: {result.get('message', 'N/A')}")
                return result.get('alert_id')
            else:
                print(f"❌ Failed to send alert: {response.status_code}")
                print(f"   Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error sending alert: {e}")
            return None
    
    def get_all_alerts(self):
        """Get all alerts from the server"""
        try:
            response = self.session.get(f"{self.base_url}/api/alerts")
            if response.status_code == 200:
                data = response.json()
                print(f"\n📊 Current Alerts in Database:")
                print(f"   Total Count: {data.get('count', 0)}")
                return data.get('alerts', [])
            else:
                print(f"❌ Failed to get alerts: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Error getting alerts: {e}")
            return []
    
    def get_system_stats(self):
        """Get system statistics"""
        try:
            response = self.session.get(f"{self.base_url}/api/stats")
            if response.status_code == 200:
                data = response.json()
                print(f"\n📈 System Statistics:")
                print(f"   Database Connected: {'✅' if data.get('database_connected') else '❌'}")
                if 'websocket_stats' in data:
                    ws_stats = data['websocket_stats']
                    print(f"   Total Connections: {ws_stats.get('total_connections', 0)}")
                    print(f"   Drone Connections: {ws_stats.get('drone_connections', 0)}")
                    print(f"   App Connections: {ws_stats.get('application_connections', 0)}")
                    print(f"   Active Alerts: {ws_stats.get('active_alerts', 0)}")
                return data
            else:
                print(f"❌ Failed to get stats: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error getting stats: {e}")
            return None

def create_test_alerts():
    """Create test alert scenarios"""
    alerts = []
    
    # Test Alert 1: Intrusion Detection
    alerts.append({
        "alert_type": "intrusion",
        "score": 0.95,
        "location": {"lat": 40.7128, "lng": -74.0060},
        "drone_id": "drone_001",
        "description": "Suspicious activity detected near main entrance"
    })
    
    # Test Alert 2: Fire Detection
    alerts.append({
        "alert_type": "fire",
        "score": 0.88,
        "location": {"lat": 40.7589, "lng": -73.9851},
        "drone_id": "drone_002",
        "description": "Smoke detected in building sector A"
    })
    
    # Test Alert 3: Object Detection
    alerts.append({
        "alert_type": "object",
        "score": 0.76,
        "location": {"lat": 40.7505, "lng": -73.9934},
        "drone_id": "drone_003",
        "description": "Unknown object detected in restricted area"
    })
    
    return alerts

def main():
    """Main test function"""
    print("🚁 Testing Local Drone Alert Server")
    print("=" * 50)
    
    # Initialize tester
    tester = LocalServerTester()
    
    # Test server health
    print("\n1. Testing server health...")
    if not tester.test_server_health():
        print("\n💡 To start the server:")
        print("   1. Make sure MongoDB is accessible")
        print("   2. Run: python main.py")
        print("   3. Or run: uvicorn main:app --host 0.0.0.0 --port 8000")
        return
    
    # Get initial stats
    print("\n2. Getting initial system stats...")
    tester.get_system_stats()
    
    # Get current alerts
    print("\n3. Getting current alerts...")
    current_alerts = tester.get_all_alerts()
    
    # Create and send test alerts
    print("\n4. Sending test alerts...")
    test_alerts = create_test_alerts()
    sent_alert_ids = []
    
    for i, alert_data in enumerate(test_alerts, 1):
        print(f"\n   Sending Alert #{i}: {alert_data['alert_type'].upper()}")
        alert_id = tester.send_alert(alert_data)
        if alert_id:
            sent_alert_ids.append(alert_id)
        time.sleep(1)
    
    # Wait a moment for processing
    print("\n5. Waiting for processing...")
    time.sleep(2)
    
    # Get updated alerts
    print("\n6. Getting updated alerts...")
    updated_alerts = tester.get_all_alerts()
    
    # Get final stats
    print("\n7. Getting final system stats...")
    tester.get_system_stats()
    
    print("\n✅ Local Server Testing Completed!")
    print(f"   Alerts sent: {len(sent_alert_ids)}")
    print(f"   Total alerts in database: {len(updated_alerts)}")
    
    print(f"\n🌐 Access Points:")
    print(f"   Dashboard: {tester.base_url}/dashboard/")
    print(f"   API Docs: {tester.base_url}/docs")
    print(f"   Health: {tester.base_url}/health")

if __name__ == "__main__":
    main() 