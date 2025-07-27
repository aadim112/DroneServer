import requests
import json

def test_railway_environment():
    """Test Railway deployment environment and database connection"""
    
    base_url = "https://web-production-190fc.up.railway.app"
    
    print("🔍 Testing Railway Environment...")
    print(f"🌐 URL: {base_url}")
    
    try:
        # Test 1: Health check
        print("\n1️⃣ Testing health endpoint...")
        health_response = requests.get(f"{base_url}/health", timeout=10)
        print(f"   Status: {health_response.status_code}")
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"   Database connected: {health_data.get('database_connected', 'Unknown')}")
            print(f"   WebSocket stats: {health_data.get('websocket_stats', {})}")
        
        # Test 2: Stats endpoint
        print("\n2️⃣ Testing stats endpoint...")
        stats_response = requests.get(f"{base_url}/api/stats", timeout=10)
        print(f"   Status: {stats_response.status_code}")
        if stats_response.status_code == 200:
            stats_data = stats_response.json()
            print(f"   Database connected: {stats_data.get('database_connected', 'Unknown')}")
            print(f"   System status: {stats_data.get('system_status', 'Unknown')}")
            print(f"   Database status: {stats_data.get('database_status', 'Unknown')}")
        
        # Test 3: Root endpoint
        print("\n3️⃣ Testing root endpoint...")
        root_response = requests.get(f"{base_url}/", timeout=10)
        print(f"   Status: {root_response.status_code}")
        if root_response.status_code == 200:
            root_data = root_response.json()
            print(f"   Message: {root_data.get('message', 'Unknown')}")
            print(f"   Status: {root_data.get('status', 'Unknown')}")
        
        # Test 4: Try to create an alert (should fail if DB not connected)
        print("\n4️⃣ Testing alert creation...")
        test_alert = {
            "drone_id": "test_drone_001",
            "alert_type": "motion_detected",
            "location": {"lat": 40.7128, "lng": -74.0060},
            "confidence": 0.95,
            "timestamp": "2025-07-27T10:20:00Z"
        }
        
        alert_response = requests.post(
            f"{base_url}/api/alerts",
            json=test_alert,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"   Status: {alert_response.status_code}")
        if alert_response.status_code == 500:
            print("   ❌ Alert creation failed (expected if DB not connected)")
        elif alert_response.status_code == 200:
            print("   ✅ Alert creation successful!")
        else:
            print(f"   Response: {alert_response.text[:100]}...")
        
        print("\n🎯 DIAGNOSIS:")
        if stats_response.status_code == 200 and not stats_data.get('database_connected', True):
            print("   ❌ Database connection failed")
            print("   💡 SOLUTION: Set environment variables in Railway dashboard")
            print("\n   Required variables:")
            print("   - MONGODB_URI")
            print("   - DATABASE_NAME")
            print("   - HOST")
            print("   - PORT")
        else:
            print("   ✅ All tests passed!")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_railway_environment() 