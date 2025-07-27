#!/usr/bin/env python3
"""
Fix Vercel Authentication Issues
"""

import subprocess
import requests
import json

def check_vercel_auth():
    """Check Vercel authentication status"""
    print("🔍 Checking Vercel Authentication Status")
    print("=" * 50)
    
    url = "https://drone-server-tau.vercel.app"
    
    print(f"Testing URL: {url}")
    
    # Test different endpoints
    endpoints = [
        ("/", "Root endpoint"),
        ("/health", "Health check"),
        ("/api/alerts", "API endpoint")
    ]
    
    for endpoint, description in endpoints:
        try:
            test_url = url + endpoint
            print(f"\n📡 Testing {description}...")
            
            response = requests.get(test_url, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ Working!")
                try:
                    data = response.json()
                    print(f"   Response: {json.dumps(data, indent=2)}")
                except:
                    print(f"   Response: {response.text[:100]}...")
            elif response.status_code == 401:
                print(f"   ❌ Authentication Required")
                print(f"   This endpoint requires authentication")
            else:
                print(f"   ❌ Failed with status {response.status_code}")
                print(f"   Response: {response.text[:100]}...")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

def provide_solutions():
    """Provide solutions for authentication issues"""
    print("\n🔧 Solutions to Fix Authentication Issues:")
    print("=" * 50)
    
    print("\n📋 Option 1: Disable Authentication in Vercel Dashboard")
    print("   1. Go to https://vercel.com/dashboard")
    print("   2. Select your project (drone-server)")
    print("   3. Go to Settings → Authentication")
    print("   4. Disable authentication or set to 'Public'")
    
    print("\n📋 Option 2: Use Vercel CLI")
    print("   1. Install Vercel CLI: npm install -g vercel")
    print("   2. Login: vercel login")
    print("   3. Link project: vercel link")
    print("   4. Configure auth: vercel env add AUTH_DISABLED true")
    
    print("\n📋 Option 3: Add Authentication Bypass")
    print("   Add this to your vercel.json:")
    print("   {")
    print('     "headers": [')
    print('       {')
    print('         "source": "/(.*)",')
    print('         "headers": [')
    print('           {')
    print('             "key": "X-Auth-Bypass",')
    print('             "value": "true"')
    print('           }')
    print('         ]')
    print('       }')
    print('     ]')
    print("   }")
    
    print("\n📋 Option 4: Create Public Preview")
    print("   1. Go to Vercel dashboard")
    print("   2. Create a new deployment")
    print("   3. Set it as public preview")
    print("   4. Use the preview URL for testing")

def test_with_auth_bypass():
    """Test with authentication bypass headers"""
    print("\n🔍 Testing with Authentication Bypass")
    print("=" * 50)
    
    url = "https://drone-server-tau.vercel.app"
    
    headers = {
        "X-Auth-Bypass": "true",
        "User-Agent": "DroneAlertTester/1.0"
    }
    
    try:
        print(f"Testing with bypass headers...")
        response = requests.get(url + "/health", headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Authentication bypass worked!")
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        else:
            print(f"❌ Still getting {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main function"""
    print("🚁 Vercel Authentication Fix")
    print("=" * 50)
    
    # Check current status
    check_vercel_auth()
    
    # Provide solutions
    provide_solutions()
    
    # Test with bypass
    test_with_auth_bypass()
    
    print("\n💡 Next Steps:")
    print("   1. Disable authentication in Vercel dashboard")
    print("   2. Or create a public preview deployment")
    print("   3. Test again with: python test_server.py")
    print("   4. Once working, you can send data to your API")

if __name__ == "__main__":
    main() 