#!/usr/bin/env python3
"""
Test Railway Server and Database
"""

import requests
import json
import time
from datetime import datetime

def test_railway_server():
    """Test Railway server endpoints"""
    print("🚁 Testing Railway Server")
    print("=" * 50)
    
    # Your Railway URL (you'll need to update this)
    base_url = "https://droneserver-production.up.railway.app"
    
    print(f"Testing URL: {base_url}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test endpoints
    endpoints = [
        ("/", "Root endpoint"),
        ("/health", "Health check"),
        ("/api/alerts", "Get alerts"),
        ("/api/stats", "Get stats"),
        ("/docs", "API documentation")
    ]
    
    for endpoint, description in endpoints:
        try:
            test_url = base_url + endpoint
            print(f"\n📡 Testing {description}...")
            
            response = requests.get(test_url, timeout=15)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ Working!")
                try:
                    data = response.json()
                    print(f"   Response: {json.dumps(data, indent=2)}")
                except:
                    print(f"   Response: {response.text[:100]}...")
            elif response.status_code == 404:
                print(f"   ❌ Not Found")
                print(f"   Response: {response.text[:100]}...")
            elif response.status_code == 500:
                print(f"   ❌ Server Error")
                print(f"   Response: {response.text[:200]}...")
            else:
                print(f"   ❌ Status {response.status_code}")
                print(f"   Response: {response.text[:100]}...")
                
        except requests.exceptions.Timeout:
            print(f"   ❌ Timeout - Server not responding")
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Connection Error - Server not reachable")
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_database_connection():
    """Test database functionality"""
    print("\n🗄️ Testing Database Connection")
    print("=" * 50)
    
    base_url = "https://droneserver-production.up.railway.app"
    
    # Test creating an alert (POST request)
    print("\n📡 Testing Database Write (Create Alert)...")
    
    test_alert = {
        "alert": "Test Alert from Railway",
        "drone_id": "test_drone_001",
        "alert_location": [40.7128, -74.0060, 100.0],
        "score": 0.85,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    try:
        response = requests.post(
            base_url + "/api/alerts",
            json=test_alert,
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            print("   ✅ Alert created successfully!")
            try:
                data = response.json()
                print(f"   Response: {json.dumps(data, indent=2)}")
                
                # Extract alert ID for further testing
                alert_id = data.get('id') or data.get('alert_id')
                if alert_id:
                    print(f"   📋 Alert ID: {alert_id}")
                    return alert_id
                    
            except:
                print(f"   Response: {response.text[:200]}...")
        else:
            print(f"   ❌ Failed to create alert")
            print(f"   Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    return None

def test_alert_retrieval(alert_id=None):
    """Test retrieving alerts from database"""
    print("\n📡 Testing Database Read (Get Alerts)...")
    
    base_url = "https://droneserver-production.up.railway.app"
    
    try:
        response = requests.get(base_url + "/api/alerts", timeout=15)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Alerts retrieved successfully!")
            try:
                data = response.json()
                alerts = data.get('alerts', [])
                print(f"   📊 Total alerts: {len(alerts)}")
                
                if alerts:
                    print(f"   📋 Latest alert:")
                    latest = alerts[0]
                    print(f"      ID: {latest.get('id', 'N/A')}")
                    print(f"      Alert: {latest.get('alert', 'N/A')}")
                    print(f"      Drone: {latest.get('drone_id', 'N/A')}")
                    print(f"      Score: {latest.get('score', 'N/A')}")
                    print(f"      Timestamp: {latest.get('timestamp', 'N/A')}")
                else:
                    print("   📋 No alerts found in database")
                    
            except Exception as e:
                print(f"   ❌ Error parsing response: {e}")
                print(f"   Response: {response.text[:200]}...")
        else:
            print(f"   ❌ Failed to retrieve alerts")
            print(f"   Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_system_stats():
    """Test system statistics"""
    print("\n📊 Testing System Statistics...")
    
    base_url = "https://droneserver-production.up.railway.app"
    
    try:
        response = requests.get(base_url + "/api/stats", timeout=15)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Stats retrieved successfully!")
            try:
                data = response.json()
                print(f"   📊 System Stats:")
                print(f"      Total Alerts: {data.get('total_alerts', 'N/A')}")
                print(f"      Active Drones: {data.get('active_drones', 'N/A')}")
                print(f"      System Status: {data.get('system_status', 'N/A')}")
                print(f"      Database Status: {data.get('database_status', 'N/A')}")
                
            except Exception as e:
                print(f"   ❌ Error parsing stats: {e}")
                print(f"   Response: {response.text[:200]}...")
        else:
            print(f"   ❌ Failed to get stats")
            print(f"   Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

def main():
    """Main function"""
    print("🚁 Railway Server & Database Test")
    print("=" * 50)
    
    # Test server endpoints
    test_railway_server()
    
    # Test database write
    alert_id = test_database_connection()
    
    # Test database read
    test_alert_retrieval(alert_id)
    
    # Test system stats
    test_system_stats()
    
    print("\n💡 Summary:")
    print("=" * 50)
    print("   ✅ Server endpoints tested")
    print("   ✅ Database write tested")
    print("   ✅ Database read tested")
    print("   ✅ System stats tested")
    
    print("\n📋 Next Steps:")
    print("   1. Check Railway dashboard for logs")
    print("   2. Verify environment variables are set")
    print("   3. Check MongoDB connection string")
    print("   4. Monitor server performance")

if __name__ == "__main__":
    main() 