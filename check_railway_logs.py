#!/usr/bin/env python3
"""
Check Railway Logs and Diagnose Issues
"""

import requests
import json
import subprocess
import os

def check_railway_status():
    """Check Railway deployment status"""
    print("🔍 Checking Railway Deployment Status")
    print("=" * 50)
    
    base_url = "https://droneserver-production.up.railway.app"
    
    print(f"Server URL: {base_url}")
    
    # Test basic connectivity
    try:
        response = requests.get(base_url, timeout=10)
        print(f"Root endpoint status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Server is responding")
            try:
                data = response.json()
                print(f"Response: {json.dumps(data, indent=2)}")
            except:
                print(f"Response: {response.text[:200]}...")
        else:
            print(f"❌ Server returned {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ Connection error: {e}")

def check_api_docs():
    """Check if API documentation is accessible"""
    print("\n📚 Checking API Documentation...")
    
    base_url = "https://droneserver-production.up.railway.app"
    
    try:
        response = requests.get(base_url + "/docs", timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API docs accessible")
            print("📋 This means FastAPI is running")
            
            # Check OpenAPI spec
            try:
                openapi_response = requests.get(base_url + "/openapi.json", timeout=10)
                if openapi_response.status_code == 200:
                    print("✅ OpenAPI spec accessible")
                    try:
                        spec = openapi_response.json()
                        paths = spec.get('paths', {})
                        print(f"📋 Available endpoints: {list(paths.keys())}")
                    except:
                        print("❌ Could not parse OpenAPI spec")
                else:
                    print(f"❌ OpenAPI spec not accessible: {openapi_response.status_code}")
            except Exception as e:
                print(f"❌ Error checking OpenAPI spec: {e}")
        else:
            print(f"❌ API docs not accessible: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def check_railway_cli():
    """Check if Railway CLI is available"""
    print("\n🔧 Checking Railway CLI...")
    
    try:
        result = subprocess.run(["railway", "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Railway CLI found: {result.stdout.strip()}")
            return True
        else:
            print("❌ Railway CLI not found")
            return False
    except FileNotFoundError:
        print("❌ Railway CLI not installed")
        return False
    except Exception as e:
        print(f"❌ Error checking Railway CLI: {e}")
        return False

def show_railway_commands():
    """Show Railway CLI commands"""
    print("\n🚀 Railway CLI Commands:")
    print("=" * 50)
    
    print("\n📋 Install Railway CLI:")
    print("   npm install -g @railway/cli")
    
    print("\n📋 Login to Railway:")
    print("   railway login")
    
    print("\n📋 Link to project:")
    print("   railway link")
    
    print("\n📋 Check status:")
    print("   railway status")
    
    print("\n📋 View logs:")
    print("   railway logs")
    
    print("\n📋 Deploy:")
    print("   railway up")
    
    print("\n📋 Check environment variables:")
    print("   railway variables")

def check_local_files():
    """Check if required files exist"""
    print("\n📋 Checking Required Files...")
    
    files_to_check = [
        ("main.py", "Main application"),
        ("Procfile", "Railway Procfile"),
        ("requirements.txt", "Python dependencies"),
        ("railway.json", "Railway configuration"),
        ("config.py", "Configuration file"),
        ("database.py", "Database manager"),
        ("models.py", "Data models")
    ]
    
    all_exist = True
    for file_path, description in files_to_check:
        if os.path.exists(file_path):
            print(f"   ✅ {description}: {file_path}")
        else:
            print(f"   ❌ {description}: {file_path} - MISSING")
            all_exist = False
    
    return all_exist

def show_troubleshooting_steps():
    """Show troubleshooting steps"""
    print("\n🔧 Troubleshooting Steps:")
    print("=" * 50)
    
    print("\n📋 Step 1: Check Railway Dashboard")
    print("   1. Go to https://railway.app/dashboard")
    print("   2. Select your project")
    print("   3. Check deployment status")
    print("   4. View logs for errors")
    
    print("\n📋 Step 2: Check Environment Variables")
    print("   1. Go to Railway dashboard")
    print("   2. Select your project")
    print("   3. Go to Variables tab")
    print("   4. Verify MONGODB_URI is set")
    
    print("\n📋 Step 3: Redeploy")
    print("   1. Push changes to GitHub")
    print("   2. Railway will auto-deploy")
    print("   3. Or use: railway up")
    
    print("\n📋 Step 4: Check Logs")
    print("   1. Use: railway logs")
    print("   2. Look for startup errors")
    print("   3. Check database connection errors")

def main():
    """Main function"""
    print("🚁 Railway Deployment Check")
    print("=" * 50)
    
    # Check Railway status
    check_railway_status()
    
    # Check API docs
    check_api_docs()
    
    # Check Railway CLI
    railway_cli_available = check_railway_cli()
    
    # Check local files
    files_ok = check_local_files()
    
    # Show commands
    show_railway_commands()
    
    # Show troubleshooting
    show_troubleshooting_steps()
    
    print("\n💡 Summary:")
    print("=" * 50)
    print(f"   Railway CLI: {'✅ Available' if railway_cli_available else '❌ Not found'}")
    print(f"   Files: {'✅ All present' if files_ok else '❌ Missing files'}")
    print("   Server: ✅ Running (docs accessible)")
    print("   API Routes: ❌ Not found (404 errors)")
    
    print("\n🎯 Next Steps:")
    print("   1. Check Railway dashboard for logs")
    print("   2. Verify environment variables")
    print("   3. Redeploy if needed")
    print("   4. Check if main.py is starting correctly")

if __name__ == "__main__":
    main() 