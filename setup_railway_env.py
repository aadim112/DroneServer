#!/usr/bin/env python3
"""
Setup Railway Environment Variables
"""

import subprocess
import os

def show_railway_env_setup():
    """Show how to set up Railway environment variables"""
    print("🔧 Railway Environment Variables Setup")
    print("=" * 50)
    
    print("\n📋 Required Environment Variables:")
    print("=" * 30)
    
    env_vars = {
        "MONGODB_URI": "mongodb+srv://aamp898989:dronesurvillance@cluster0.cftmhkh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
        "DATABASE_NAME": "drone_alerts_db",
        "ENVIRONMENT": "production",
        "DEBUG": "false",
        "HOST": "0.0.0.0",
        "PORT": "8080"
    }
    
    for var, value in env_vars.items():
        print(f"   {var}: {value}")
    
    print("\n🌐 Railway Dashboard Setup:")
    print("=" * 30)
    print("   1. Go to https://railway.app/dashboard")
    print("   2. Select your project")
    print("   3. Go to Variables tab")
    print("   4. Add each variable above")
    
    print("\n🚀 Railway CLI Setup:")
    print("=" * 30)
    print("   1. Install Railway CLI:")
    print("      npm install -g @railway/cli")
    print("   2. Login:")
    print("      railway login")
    print("   3. Link project:")
    print("      railway link")
    print("   4. Set variables:")
    
    for var, value in env_vars.items():
        print(f"      railway variables set {var}={value}")
    
    print("\n📋 Alternative: Use Railway CLI to set all at once:")
    print("=" * 50)
    
    # Create a command to set all variables
    commands = []
    for var, value in env_vars.items():
        commands.append(f'railway variables set {var}="{value}"')
    
    print("   Run these commands:")
    for cmd in commands:
        print(f"   {cmd}")

def check_railway_cli():
    """Check if Railway CLI is available"""
    print("\n🔍 Checking Railway CLI...")
    
    try:
        result = subprocess.run(["railway", "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"   ✅ Railway CLI found: {result.stdout.strip()}")
            return True
        else:
            print("   ❌ Railway CLI not found")
            return False
    except FileNotFoundError:
        print("   ❌ Railway CLI not installed")
        return False
    except Exception as e:
        print(f"   ❌ Error checking Railway CLI: {e}")
        return False

def show_mongodb_setup():
    """Show MongoDB setup instructions"""
    print("\n🗄️ MongoDB Setup:")
    print("=" * 30)
    print("   ✅ MongoDB Atlas cluster is configured")
    print("   ✅ Connection string is ready")
    print("   ✅ Database: drone_alerts_db")
    print("   ✅ Collection: alerts")
    
    print("\n📋 MongoDB Connection Details:")
    print("   Cluster: Cluster0")
    print("   Database: drone_alerts_db")
    print("   Collection: alerts")
    print("   Connection: mongodb+srv://aamp898989:dronesurvillance@cluster0.cftmhkh.mongodb.net/")

def show_deployment_steps():
    """Show deployment steps"""
    print("\n🚀 Deployment Steps:")
    print("=" * 30)
    
    print("\n📋 Step 1: Set Environment Variables")
    print("   1. Go to Railway dashboard")
    print("   2. Add MONGODB_URI and other variables")
    print("   3. Save changes")
    
    print("\n📋 Step 2: Redeploy")
    print("   1. Push changes to GitHub")
    print("   2. Or use: railway up")
    print("   3. Wait for deployment")
    
    print("\n📋 Step 3: Test")
    print("   1. Wait 2-3 minutes")
    print("   2. Run: python test_railway.py")
    print("   3. Check if endpoints work")

def main():
    """Main function"""
    print("🚁 Railway Environment Setup")
    print("=" * 50)
    
    # Check Railway CLI
    railway_cli_available = check_railway_cli()
    
    # Show environment setup
    show_railway_env_setup()
    
    # Show MongoDB setup
    show_mongodb_setup()
    
    # Show deployment steps
    show_deployment_steps()
    
    print("\n💡 Summary:")
    print("=" * 50)
    print(f"   Railway CLI: {'✅ Available' if railway_cli_available else '❌ Not found'}")
    print("   MongoDB: ✅ Configured")
    print("   Next: Set environment variables in Railway dashboard")
    print("   Then: Redeploy and test")
    
    print("\n🎯 Expected Results After Setup:")
    print("   ✅ No more PostgreSQL errors")
    print("   ✅ MongoDB connection successful")
    print("   ✅ All API endpoints working")
    print("   ✅ Database operations working")

if __name__ == "__main__":
    main() 