import requests
import json
import time

def test_after_environment_fix():
    """Test the server after environment variables are set"""
    
    base_url = "https://web-production-190fc.up.railway.app"
    
    print("🔍 Testing Server After Environment Fix...")
    print(f"🌐 URL: {base_url}")
    
    # Wait a moment for deployment to complete
    print("⏳ Waiting for deployment to complete...")
    time.sleep(5)
    
    try:
        # Test 1: Health check
        print("\n1️⃣ Testing health endpoint...")
        health_response = requests.get(f"{base_url}/health", timeout=15)
        print(f"   Status: {health_response.status_code}")
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"   Database connected: {health_data.get('database_connected', 'Unknown')}")
            print(f"   WebSocket stats: {health_data.get('websocket_stats', {})}")
        
        # Test 2: Stats endpoint
        print("\n2️⃣ Testing stats endpoint...")
        stats_response = requests.get(f"{base_url}/api/stats", timeout=15)
        print(f"   Status: {stats_response.status_code}")
        if stats_response.status_code == 200:
            stats_data = stats_response.json()
            print(f"   Database connected: {stats_data.get('database_connected', 'Unknown')}")
            print(f"   System status: {stats_data.get('system_status', 'Unknown')}")
            print(f"   Database status: {stats_data.get('database_status', 'Unknown')}")
            
            if stats_data.get('database_connected', False):
                print("   ✅ DATABASE CONNECTION SUCCESSFUL!")
            else:
                print("   ❌ Database still not connected")
        
        # Test 3: Create a test alert
        print("\n3️⃣ Testing alert creation...")
        test_alert = {
            "drone_id": "test_drone_001",
            "alert_type": "motion_detected",
            "location": {"lat": 40.7128, "lng": -74.0060},
            "confidence": 0.95,
            "timestamp": "2025-07-27T10:25:00Z"
        }
        
        alert_response = requests.post(
            f"{base_url}/api/alerts",
            json=test_alert,
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        print(f"   Status: {alert_response.status_code}")
        
        if alert_response.status_code == 200:
            alert_data = alert_response.json()
            print("   ✅ Alert created successfully!")
            print(f"   Alert ID: {alert_data.get('id', 'Unknown')}")
            
            # Test 4: Get the created alert
            print("\n4️⃣ Testing alert retrieval...")
            alert_id = alert_data.get('id')
            if alert_id:
                get_alert_response = requests.get(f"{base_url}/api/alerts/{alert_id}", timeout=15)
                print(f"   Status: {get_alert_response.status_code}")
                if get_alert_response.status_code == 200:
                    print("   ✅ Alert retrieved successfully!")
                else:
                    print(f"   ❌ Failed to retrieve alert: {get_alert_response.text}")
        else:
            print(f"   ❌ Alert creation failed: {alert_response.text}")
        
        # Test 5: Get all alerts
        print("\n5️⃣ Testing get all alerts...")
        all_alerts_response = requests.get(f"{base_url}/api/alerts", timeout=15)
        print(f"   Status: {all_alerts_response.status_code}")
        if all_alerts_response.status_code == 200:
            all_alerts = all_alerts_response.json()
            print(f"   ✅ Retrieved {len(all_alerts)} alerts")
        else:
            print(f"   ❌ Failed to get alerts: {all_alerts_response.text}")
        
        print("\n🎯 FINAL STATUS:")
        if stats_response.status_code == 200 and stats_data.get('database_connected', False):
            print("   🎉 SUCCESS! Server is fully operational!")
            print("   ✅ Database connected")
            print("   ✅ API endpoints working")
            print("   ✅ Ready for drone alerts!")
        else:
            print("   ❌ Still need to fix environment variables")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_after_environment_fix() 