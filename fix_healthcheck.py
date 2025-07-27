#!/usr/bin/env python3
"""
Fix Healthcheck Issues
"""

import requests
import time
import json

def test_new_deployment():
    """Test the new Railway deployment"""
    print("🔍 Testing New Railway Deployment")
    print("=" * 50)
    
    # Update this URL with your new Railway project URL
    base_url = "https://web-production-190fc.up.railway.app"  # UPDATE THIS
    
    print(f"Testing URL: {base_url}")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test basic connectivity
    print("\n📡 Testing Basic Connectivity...")
    try:
        response = requests.get(base_url, timeout=15)
        print(f"   Root endpoint status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Server is responding!")
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

def show_railway_logs_check():
    """Show how to check Railway logs"""
    print("\n📋 Check Railway Logs:")
    print("=" * 30)
    
    print("1. Go to Railway dashboard")
    print("2. Select your new project")
    print("3. Go to Deployments tab")
    print("4. Click on the latest deployment")
    print("5. Check both Build Logs and Runtime Logs")
    
    print("\n🔍 Look for these errors:")
    print("   ❌ Import errors")
    print("   ❌ MongoDB connection failed")
    print("   ❌ Missing dependencies")
    print("   ❌ Port already in use")
    print("   ❌ Environment variable errors")

def show_environment_variables():
    """Show required environment variables"""
    print("\n⚙️ Required Environment Variables:")
    print("=" * 40)
    
    variables = {
        "MONGODB_URI": "mongodb+srv://aamp898989:dronesurvillance@cluster0.cftmhkh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
        "DATABASE_NAME": "drone_alerts_db",
        "ENVIRONMENT": "production",
        "DEBUG": "false",
        "HOST": "0.0.0.0",
        "PORT": "8080"
    }
    
    print("Add these in Railway Variables tab:")
    for var, value in variables.items():
        print(f"   {var} = {value}")

def show_railway_cli_fix():
    """Show Railway CLI fix commands"""
    print("\n🚀 Railway CLI Fix Commands:")
    print("=" * 30)
    
    print("If you have Railway CLI installed:")
    print("   npm install -g @railway/cli")
    print("   railway login")
    print("   railway link")
    print("   railway variables set MONGODB_URI=\"mongodb+srv://aamp898989:dronesurvillance@cluster0.cftmhkh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0\"")
    print("   railway variables set DATABASE_NAME=\"drone_alerts_db\"")
    print("   railway variables set ENVIRONMENT=\"production\"")
    print("   railway variables set DEBUG=\"false\"")
    print("   railway variables set HOST=\"0.0.0.0\"")
    print("   railway variables set PORT=\"8080\"")
    print("   railway up")

def show_common_fixes():
    """Show common fixes for healthcheck issues"""
    print("\n🔧 Common Healthcheck Fixes:")
    print("=" * 35)
    
    print("\n📋 Fix 1: Environment Variables")
    print("   - Set all required environment variables")
    print("   - Ensure MONGODB_URI is correct")
    print("   - Check for typos in variable names")
    
    print("\n📋 Fix 2: Dependencies")
    print("   - Check if requirements.txt is correct")
    print("   - Ensure all packages are installed")
    print("   - Look for missing dependencies in logs")
    
    print("\n📋 Fix 3: Application Startup")
    print("   - Check if main.py starts correctly")
    print("   - Look for import errors")
    print("   - Verify database connection")
    
    print("\n📋 Fix 4: Port Configuration")
    print("   - Ensure PORT=8080 is set")
    print("   - Check if port is available")
    print("   - Verify HOST=0.0.0.0")

def show_expected_logs():
    """Show expected successful logs"""
    print("\n✅ Expected Successful Logs:")
    print("=" * 35)
    
    print("Look for these messages in Railway logs:")
    print("   ✅ 'Starting Drone Alert Management System...'")
    print("   ✅ 'Database connected successfully'")
    print("   ✅ 'System started successfully'")
    print("   ✅ 'Application startup complete'")
    print("   ✅ 'Uvicorn running on http://0.0.0.0:8080'")
    print("   ✅ 'INFO: Application startup complete'")

def main():
    """Main function"""
    print("🚁 Fix Healthcheck Issues")
    print("=" * 50)
    
    # Test deployment
    test_new_deployment()
    
    # Show logs check
    show_railway_logs_check()
    
    # Show environment variables
    show_environment_variables()
    
    # Show CLI fix
    show_railway_cli_fix()
    
    # Show common fixes
    show_common_fixes()
    
    # Show expected logs
    show_expected_logs()
    
    print("\n💡 Immediate Actions:")
    print("=" * 25)
    print("1. 🔍 Check Railway logs for errors")
    print("2. ⚙️ Set environment variables")
    print("3. 🔄 Redeploy if needed")
    print("4. 🧪 Test after deployment")
    
    print("\n🎯 Most Common Issue:")
    print("   Missing or incorrect MONGODB_URI environment variable")

if __name__ == "__main__":
    main() 