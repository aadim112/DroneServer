#!/usr/bin/env python3
"""
Simple Server Test - Test the drone alert server
"""

import requests
import json

def test_server(base_url="http://droneserver-production.up.railway.app"):
    """Test server endpoints"""
    print(f"🚁 Testing Server: {base_url}")
    print("=" * 50)
    
    # Test basic endpoints
    endpoints = [
        ("/", "Root endpoint"),
        ("/health", "Health check"),
        ("/api/alerts", "Get alerts"),
        ("/api/stats", "Get stats")
    ]
    
    for endpoint, description in endpoints:
        try:
            url = base_url + endpoint
            print(f"\n📡 Testing {description}...")
            
            response = requests.get(url, timeout=5)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ Working!")
                if endpoint == "/":
                    try:
                        data = response.json()
                        print(f"   Response: {json.dumps(data, indent=2)}")
                    except:
                        print(f"   Response: {response.text[:100]}...")
            else:
                print(f"   ❌ Failed")
                print(f"   Response: {response.text[:100]}...")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Connection Error - Server not running")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Test POST request
    print(f"\n📡 Testing POST /api/alerts...")
    try:
        test_alert = {
            "alert_type": "test",
            "score": 0.85,
            "location": {"lat": 40.7128, "lng": -74.0060},
            "drone_id": "test_drone",
            "description": "Test alert"
        }
        
        response = requests.post(
            f"{base_url}/api/alerts",
            json=test_alert,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Alert created successfully!")
            print(f"   Alert ID: {result.get('alert_id', 'N/A')}")
        else:
            print(f"   ❌ Failed to create alert")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    import sys
    
    # Check if URL provided as argument
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = "https://droneserver-production.up.railway.app"
    
    test_server(url) 