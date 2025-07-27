#!/usr/bin/env python3
"""
Debug Server Issues - Identify problems with the deployed server
"""

import requests
import json
import base64

def test_server_health():
    """Test basic server connectivity"""
    base_url = "https://droneserver-production.up.railway.app"
    
    print("🔍 Debugging Server Issues")
    print("=" * 50)
    print(f"Server URL: {base_url}")
    
    # Test 1: Basic connectivity
    print("\n1. Testing basic connectivity...")
    try:
        response = requests.get(f"{base_url}/docs", timeout=10)
        print(f"   ✅ Server is reachable (docs: {response.status_code})")
    except Exception as e:
        print(f"   ❌ Server connectivity issue: {e}")
        return
    
    # Test 2: Check OpenAPI spec for exact requirements
    print("\n2. Checking API specification...")
    try:
        response = requests.get(f"{base_url}/openapi.json", timeout=10)
        if response.status_code == 200:
            spec = response.json()
            print(f"   ✅ OpenAPI spec retrieved")
            
            # Check required parameters for each endpoint
            paths = spec.get('paths', {})
            for path, methods in paths.items():
                print(f"\n   📍 Endpoint: {path}")
                for method, details in methods.items():
                    if method.upper() == 'POST':
                        params = details.get('parameters', [])
                        required_params = [p['name'] for p in params if p.get('required', False)]
                        print(f"      {method.upper()}: Required params: {required_params}")
                        
                        # Check request body
                        request_body = details.get('requestBody', {})
                        if request_body:
                            content = request_body.get('content', {})
                            for content_type, schema in content.items():
                                print(f"      Content-Type: {content_type}")
                                if 'schema' in schema:
                                    print(f"      Schema: {schema['schema']}")
        else:
            print(f"   ❌ Failed to get OpenAPI spec: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error getting OpenAPI spec: {e}")
    
    # Test 3: Try minimal requests
    print("\n3. Testing minimal requests...")
    
    # Test group creation with minimal data
    print("\n   Testing group creation...")
    try:
        url = f"{base_url}/api/v1/groups/create/"
        params = {
            "region": "test",
            "purpose": "test",
            "rl_model_instance": "test"
        }
        response = requests.post(url, params=params, timeout=10)
        print(f"      Status: {response.status_code}")
        print(f"      Response: {response.text[:200]}")
    except Exception as e:
        print(f"      Error: {e}")
    
    # Test drone registration with minimal data
    print("\n   Testing drone registration...")
    try:
        url = f"{base_url}/api/v1/drones/register/"
        params = {
            "drone_id": 1,
            "location": "test",
            "purpose": "test"
        }
        response = requests.post(url, params=params, timeout=10)
        print(f"      Status: {response.status_code}")
        print(f"      Response: {response.text[:200]}")
    except Exception as e:
        print(f"      Error: {e}")
    
    # Test data upload with minimal data
    print("\n   Testing data upload...")
    try:
        url = f"{base_url}/api/v1/drones/data/"
        
        # Create a minimal test image
        minimal_image = base64.b64encode(b"test_image_data").decode()
        
        data = {
            "drone_id": 1,
            "location": "test",
            "score": 0.5,
            "casuality": "test"
        }
        
        files = {
            "image": ("test.jpg", minimal_image, "image/jpeg")
        }
        
        response = requests.post(url, data=data, files=files, timeout=10)
        print(f"      Status: {response.status_code}")
        print(f"      Response: {response.text[:200]}")
    except Exception as e:
        print(f"      Error: {e}")
    
    # Test 4: Check server logs or error details
    print("\n4. Checking for detailed error information...")
    try:
        # Try to get more detailed error response
        url = f"{base_url}/api/v1/drones/data/"
        response = requests.get(url, timeout=10)
        print(f"   GET /api/v1/drones/data/ - Status: {response.status_code}")
        if response.status_code != 200:
            print(f"   Error details: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print(f"\n🔧 Troubleshooting Steps:")
    print(f"   1. Check Railway deployment logs")
    print(f"   2. Verify database connection")
    print(f"   3. Check environment variables")
    print(f"   4. Ensure all dependencies are installed")
    print(f"   5. Check if the server is running the correct code")

if __name__ == "__main__":
    test_server_health() 