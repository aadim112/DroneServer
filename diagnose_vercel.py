#!/usr/bin/env python3
"""
Diagnose Vercel Deployment Issues
"""

import requests
import json
import time

def test_vercel_deployment():
    """Test Vercel deployment thoroughly"""
    print("🔍 Diagnosing Vercel Deployment")
    print("=" * 50)
    
    base_url = "https://drone-server-tau.vercel.app"
    
    print(f"Testing URL: {base_url}")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test basic connectivity
    print("\n📡 Testing Basic Connectivity...")
    try:
        response = requests.get(base_url, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        print(f"   Content-Type: {response.headers.get('content-type', 'unknown')}")
        
        if response.status_code == 200:
            print("   ✅ Server is responding")
            try:
                data = response.json()
                print(f"   Response: {json.dumps(data, indent=2)}")
            except:
                print(f"   Response: {response.text[:200]}...")
        else:
            print(f"   ❌ Server returned {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
    
    # Test different paths
    print("\n📡 Testing Different Paths...")
    paths = [
        ("/", "Root"),
        ("/health", "Health"),
        ("/api/alerts", "API Alerts"),
        ("/docs", "API Docs"),
        ("/openapi.json", "OpenAPI Spec"),
        ("/api", "API Root"),
        ("/test", "Non-existent path")
    ]
    
    for path, description in paths:
        try:
            test_url = base_url + path
            print(f"\n   Testing {description} ({path})...")
            
            response = requests.get(test_url, timeout=10)
            print(f"      Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"      ✅ Working!")
                if path in ["/docs", "/openapi.json"]:
                    print(f"      Content-Type: {response.headers.get('content-type')}")
                else:
                    try:
                        data = response.json()
                        print(f"      Response: {json.dumps(data, indent=4)}")
                    except:
                        print(f"      Response: {response.text[:100]}...")
            elif response.status_code == 404:
                print(f"      ❌ Not Found")
                print(f"      Response: {response.text[:100]}...")
            else:
                print(f"      ❌ Status {response.status_code}")
                print(f"      Response: {response.text[:100]}...")
                
        except Exception as e:
            print(f"      ❌ Error: {e}")
    
    # Test POST request
    print("\n📡 Testing POST Request...")
    try:
        test_data = {
            "alert": "Test Alert",
            "drone_id": "test_drone",
            "alert_location": [0, 0, 0],
            "score": 0.5,
            "timestamp": "2025-07-27T13:15:00Z"
        }
        
        response = requests.post(
            base_url + "/api/alerts",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        
        if response.status_code in [200, 201]:
            print("   ✅ POST request successful!")
            try:
                data = response.json()
                print(f"   Response: {json.dumps(data, indent=2)}")
            except:
                print(f"   Response: {response.text[:200]}...")
        else:
            print(f"   ❌ POST failed with status {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"   ❌ POST error: {e}")

def check_vercel_config():
    """Check Vercel configuration"""
    print("\n🔧 Vercel Configuration Check")
    print("=" * 50)
    
    print("📋 Current vercel.json configuration:")
    try:
        with open("vercel.json", "r") as f:
            config = json.load(f)
            print(json.dumps(config, indent=2))
    except Exception as e:
        print(f"   ❌ Error reading vercel.json: {e}")
    
    print("\n📋 Checking main_vercel.py exists:")
    try:
        with open("main_vercel.py", "r") as f:
            first_line = f.readline().strip()
            print(f"   ✅ main_vercel.py exists")
            print(f"   First line: {first_line}")
    except Exception as e:
        print(f"   ❌ Error reading main_vercel.py: {e}")

def provide_solutions():
    """Provide solutions for 404 issues"""
    print("\n🔧 Solutions for 404 Issues:")
    print("=" * 50)
    
    print("\n📋 Option 1: Check Vercel Dashboard")
    print("   1. Go to https://vercel.com/dashboard")
    print("   2. Select your project")
    print("   3. Check deployment logs for errors")
    print("   4. Verify the deployment is successful")
    
    print("\n📋 Option 2: Redeploy with Vercel CLI")
    print("   1. Install Vercel CLI: npm install -g vercel")
    print("   2. Login: vercel login")
    print("   3. Link project: vercel link")
    print("   4. Deploy: vercel --prod")
    
    print("\n📋 Option 3: Check Function Logs")
    print("   1. Go to Vercel dashboard")
    print("   2. Select your project")
    print("   3. Go to Functions tab")
    print("   4. Check for any errors in main_vercel.py")
    
    print("\n📋 Option 4: Simplify Configuration")
    print("   Try this simplified vercel.json:")
    print("   {")
    print('     "version": 2,')
    print('     "builds": [')
    print('       {')
    print('         "src": "main_vercel.py",')
    print('         "use": "@vercel/python"')
    print('       }')
    print('     ],')
    print('     "routes": [')
    print('       {')
    print('         "src": "/(.*)",')
    print('         "dest": "/main_vercel.py"')
    print('       }')
    print('     ]')
    print("   }")

def main():
    """Main function"""
    print("🚁 Vercel Deployment Diagnosis")
    print("=" * 50)
    
    # Test deployment
    test_vercel_deployment()
    
    # Check configuration
    check_vercel_config()
    
    # Provide solutions
    provide_solutions()
    
    print("\n💡 Next Steps:")
    print("   1. Check Vercel dashboard for deployment logs")
    print("   2. Redeploy using Vercel CLI")
    print("   3. Check if main_vercel.py is being found")
    print("   4. Verify environment variables are set")

if __name__ == "__main__":
    main() 