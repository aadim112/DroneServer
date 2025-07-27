#!/usr/bin/env python3
"""
API Discovery - Find the correct endpoints on the deployed server
"""

import requests
import json

def discover_api():
    base_url = "https://droneserver-production.up.railway.app"
    
    print("🔍 API Discovery - Finding Correct Endpoints")
    print("=" * 50)
    print(f"Server URL: {base_url}")
    
    # Try different possible API paths
    possible_paths = [
        "/",
        "/api/alerts",
        "/alerts", 
        "/api/v1/alerts",
        "/v1/alerts",
        "/health",
        "/api/health",
        "/status",
        "/api/status",
        "/stats",
        "/api/stats"
    ]
    
    working_endpoints = []
    
    for path in possible_paths:
        try:
            url = base_url + path
            print(f"\n📡 Testing: {path}")
            
            response = requests.get(url, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ Working!")
                working_endpoints.append(path)
                
                # Try to parse JSON response
                try:
                    data = response.json()
                    if isinstance(data, dict):
                        print(f"   Response keys: {list(data.keys())}")
                        if 'message' in data:
                            print(f"   Message: {data['message']}")
                except:
                    print(f"   Response: {response.text[:100]}...")
                    
            elif response.status_code == 404:
                print(f"   ❌ Not Found")
            else:
                print(f"   ⚠️  Status: {response.status_code}")
                print(f"   Response: {response.text[:100]}...")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Connection Error")
        except requests.exceptions.Timeout:
            print(f"   ⏰ Timeout")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n📋 Summary:")
    print(f"   Working endpoints: {len(working_endpoints)}")
    for endpoint in working_endpoints:
        print(f"   ✅ {endpoint}")
    
    # Try to get OpenAPI docs
    print(f"\n📚 Checking API Documentation:")
    try:
        docs_url = base_url + "/docs"
        response = requests.get(docs_url, timeout=10)
        if response.status_code == 200:
            print(f"   ✅ API Docs available at: {docs_url}")
            print(f"   📖 OpenAPI JSON at: {base_url}/openapi.json")
        else:
            print(f"   ❌ API Docs not found")
    except Exception as e:
        print(f"   ❌ Error accessing docs: {e}")
    
    print(f"\n🌐 Next Steps:")
    print(f"   1. Visit {base_url}/docs in your browser")
    print(f"   2. Check the OpenAPI specification")
    print(f"   3. Use the working endpoints for testing")

if __name__ == "__main__":
    discover_api() 