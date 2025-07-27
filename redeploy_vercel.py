#!/usr/bin/env python3
"""
Redeploy to Vercel with Fixed Configuration
"""

import subprocess
import os
import json

def check_vercel_cli():
    """Check if Vercel CLI is installed"""
    print("🔍 Checking Vercel CLI...")
    try:
        result = subprocess.run(["vercel", "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"   ✅ Vercel CLI found: {result.stdout.strip()}")
            return True
        else:
            print("   ❌ Vercel CLI not found")
            return False
    except FileNotFoundError:
        print("   ❌ Vercel CLI not installed")
        return False
    except Exception as e:
        print(f"   ❌ Error checking Vercel CLI: {e}")
        return False

def check_files():
    """Check if required files exist"""
    print("\n📋 Checking Required Files...")
    
    files_to_check = [
        ("api/index.py", "API Function"),
        ("api/requirements.txt", "API Requirements"),
        ("vercel.json", "Vercel Configuration")
    ]
    
    all_exist = True
    for file_path, description in files_to_check:
        if os.path.exists(file_path):
            print(f"   ✅ {description}: {file_path}")
        else:
            print(f"   ❌ {description}: {file_path} - MISSING")
            all_exist = False
    
    return all_exist

def show_deployment_steps():
    """Show manual deployment steps"""
    print("\n🚀 Manual Deployment Steps:")
    print("=" * 50)
    
    print("\n📋 Step 1: Install Vercel CLI (if not installed)")
    print("   npm install -g vercel")
    
    print("\n📋 Step 2: Login to Vercel")
    print("   vercel login")
    
    print("\n📋 Step 3: Link to your project")
    print("   vercel link")
    
    print("\n📋 Step 4: Deploy to production")
    print("   vercel --prod")
    
    print("\n📋 Alternative: Deploy via GitHub")
    print("   1. Push your changes to GitHub")
    print("   2. Vercel will auto-deploy")
    print("   3. Check deployment status in dashboard")

def show_configuration():
    """Show current configuration"""
    print("\n⚙️ Current Configuration:")
    print("=" * 50)
    
    print("\n📋 vercel.json:")
    try:
        with open("vercel.json", "r") as f:
            config = json.load(f)
            print(json.dumps(config, indent=2))
    except Exception as e:
        print(f"   ❌ Error reading vercel.json: {e}")
    
    print("\n📋 api/index.py (first 10 lines):")
    try:
        with open("api/index.py", "r") as f:
            lines = f.readlines()[:10]
            for i, line in enumerate(lines, 1):
                print(f"   {i:2d}: {line.rstrip()}")
    except Exception as e:
        print(f"   ❌ Error reading api/index.py: {e}")

def test_local():
    """Test the API locally"""
    print("\n🧪 Testing API Locally...")
    print("=" * 50)
    
    try:
        # Import and test the app
        import sys
        sys.path.append('api')
        
        from index import app
        
        print("   ✅ API imported successfully")
        print(f"   📋 Available routes:")
        
        for route in app.routes:
            if hasattr(route, 'path'):
                methods = [method for method in ['GET', 'POST', 'PUT', 'DELETE'] 
                          if hasattr(route, method.lower())]
                print(f"      {route.path} - {', '.join(methods)}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error testing API: {e}")
        return False

def main():
    """Main function"""
    print("🚁 Vercel Redeployment Helper")
    print("=" * 50)
    
    # Check Vercel CLI
    vercel_available = check_vercel_cli()
    
    # Check files
    files_ok = check_files()
    
    # Show configuration
    show_configuration()
    
    # Test locally
    local_test_ok = test_local()
    
    # Show deployment steps
    show_deployment_steps()
    
    print("\n💡 Summary:")
    print("=" * 50)
    print(f"   Vercel CLI: {'✅ Available' if vercel_available else '❌ Not found'}")
    print(f"   Files: {'✅ All present' if files_ok else '❌ Missing files'}")
    print(f"   Local Test: {'✅ Passed' if local_test_ok else '❌ Failed'}")
    
    if vercel_available and files_ok and local_test_ok:
        print("\n🎉 Ready to deploy!")
        print("   Run: vercel --prod")
    else:
        print("\n⚠️ Please fix issues before deploying")
    
    print("\n📋 After deployment, test with:")
    print("   python test_server.py")

if __name__ == "__main__":
    main() 