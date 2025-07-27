#!/usr/bin/env python3
"""
Simple test to check deployed server status
"""

import requests
import json

def test_server():
    base_url = "https://droneserver-production.up.railway.app"
    
    print("🔍 Testing Deployed Server Status")
    print("=" * 40)
    print(f"Server URL: {base_url}")
    
    # Test different endpoints
    endpoints = [
        "/",
        "/health", 
        "/api/alerts",
        "/api/stats",
        "/docs",
        "/dashboard/"
    ]
    
    for endpoint in endpoints:
        try:
            url = base_url + endpoint
            print(f"\n📡 Testing: {endpoint}")
            
            response = requests.get(url, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ Success!")
                if endpoint == "/":
                    try:
                        data = response.json()
                        print(f"   Response: {json.dumps(data, indent=2)}")
                    except:
                        print(f"   Response: {response.text[:200]}...")
            else:
                print(f"   ❌ Failed")
                print(f"   Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Connection Error - Server might be down")
        except requests.exceptions.Timeout:
            print(f"   ⏰ Timeout - Server is slow to respond")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n🌐 Try accessing these URLs in your browser:")
    print(f"   Main: {base_url}/")
    print(f"   API Docs: {base_url}/docs")
    print(f"   Dashboard: {base_url}/dashboard/")

if __name__ == "__main__":
    test_server() 