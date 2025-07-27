#!/usr/bin/env python3
"""
Diagnose Healthcheck Issues
"""

import requests
import time
import json

def test_railway_healthcheck():
    """Test Railway healthcheck endpoint"""
    print("🔍 Diagnosing Healthcheck Issues")
    print("=" * 50)
    
    # Your Railway URL (update this with your new project URL)
    base_url = "https://droneserver-production.up.railway.app"
    
    print(f"Testing URL: {base_url}")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test basic connectivity
    print("\n📡 Testing Basic Connectivity...")
    try:
        response = requests.get(base_url, timeout=10)
        print(f"   Root endpoint status: {response.status_code}")
        
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
            
    except requests.exceptions.Timeout:
        print("   ❌ Timeout - Server not responding")
    except requests.exceptions.ConnectionError:
        print("   ❌ Connection Error - Server not reachable")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test health endpoint specifically
    print("\n📡 Testing Health Endpoint...")
    try:
        health_url = base_url + "/health"
        response = requests.get(health_url, timeout=10)
        print(f"   Health endpoint status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Health endpoint working!")
            try:
                data = response.json()
                print(f"   Response: {json.dumps(data, indent=2)}")
            except:
                print(f"   Response: {response.text[:200]}...")
        else:
            print(f"   ❌ Health endpoint failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            
    except requests.exceptions.Timeout:
        print("   ❌ Health endpoint timeout")
    except requests.exceptions.ConnectionError:
        print("   ❌ Health endpoint connection error")
    except Exception as e:
        print(f"   ❌ Health endpoint error: {e}")
    
    # Test other endpoints
    print("\n📡 Testing Other Endpoints...")
    endpoints = [
        ("/", "Root"),
        ("/docs", "API Docs"),
        ("/api/alerts", "API Alerts"),
        ("/api/stats", "API Stats")
    ]
    
    for endpoint, description in endpoints:
        try:
            test_url = base_url + endpoint
            response = requests.get(test_url, timeout=10)
            print(f"   {description}: {response.status_code}")
        except Exception as e:
            print(f"   {description}: Error - {e}")

def show_railway_troubleshooting():
    """Show Railway troubleshooting steps"""
    print("\n🔧 Railway Troubleshooting Steps:")
    print("=" * 50)
    
    print("\n📋 Step 1: Check Railway Logs")
    print("   1. Go to Railway dashboard")
    print("   2. Select your project")
    print("   3. Go to Deployments tab")
    print("   4. Click on latest deployment")
    print("   5. Check build logs and runtime logs")
    
    print("\n📋 Step 2: Check Environment Variables")
    print("   1. Go to Variables tab")
    print("   2. Verify these are set:")
    print("      MONGODB_URI=mongodb+srv://...")
    print("      DATABASE_NAME=drone_alerts_db")
    print("      ENVIRONMENT=production")
    print("      DEBUG=false")
    print("      HOST=0.0.0.0")
    print("      PORT=8080")
    
    print("\n📋 Step 3: Check Application Startup")
    print("   Look for these in logs:")
    print("   ✅ 'Starting Drone Alert Management System...'")
    print("   ✅ 'Database connected successfully'")
    print("   ✅ 'Application startup complete'")
    print("   ✅ 'Uvicorn running on http://0.0.0.0:8080'")
    
    print("\n📋 Step 4: Common Issues")
    print("   ❌ MongoDB connection failed")
    print("   ❌ Missing dependencies")
    print("   ❌ Port conflicts")
    print("   ❌ Import errors")

def show_healthcheck_config():
    """Show healthcheck configuration"""
    print("\n⚙️ Healthcheck Configuration:")
    print("=" * 40)
    
    print("Current railway.json settings:")
    print("   healthcheckPath: /health")
    print("   healthcheckTimeout: 120 seconds")
    print("   startCommand: python main.py")
    
    print("\n📋 Healthcheck Process:")
    print("   1. Railway starts the application")
    print("   2. Waits for server to be ready")
    print("   3. Makes GET request to /health")
    print("   4. Expects 200 OK response")
    print("   5. Retries for 2 minutes if fails")

def main():
    """Main function"""
    print("🚁 Healthcheck Diagnosis")
    print("=" * 50)
    
    # Test healthcheck
    test_railway_healthcheck()
    
    # Show troubleshooting
    show_railway_troubleshooting()
    
    # Show healthcheck config
    show_healthcheck_config()
    
    print("\n💡 Next Steps:")
    print("=" * 30)
    print("1. Check Railway logs for startup errors")
    print("2. Verify environment variables are set")
    print("3. Check if MongoDB connection is working")
    print("4. Look for any import or dependency errors")
    
    print("\n🎯 Common Solutions:")
    print("   - Set correct environment variables")
    print("   - Fix MongoDB connection string")
    print("   - Check for missing dependencies")
    print("   - Verify main.py starts correctly")

if __name__ == "__main__":
    main() 