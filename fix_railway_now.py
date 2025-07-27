#!/usr/bin/env python3
"""
Quick Fix for Railway Environment Variables
"""

import subprocess
import time

def show_immediate_fix():
    """Show immediate fix steps"""
    print("🚨 IMMEDIATE FIX FOR RAILWAY")
    print("=" * 50)
    
    print("\n❌ Current Issues:")
    print("   - PostgreSQL connection errors")
    print("   - DATABASE_URL not configured")
    print("   - API endpoints returning 404")
    print("   - Server running but routes not working")
    
    print("\n✅ Solution: Set Environment Variables in Railway Dashboard")
    print("=" * 60)
    
    print("\n📋 Step 1: Go to Railway Dashboard")
    print("   URL: https://railway.app/dashboard")
    print("   Select your project")
    print("   Go to Variables tab")
    
    print("\n📋 Step 2: Add These Variables (Copy & Paste):")
    print("=" * 40)
    
    variables = [
        ("MONGODB_URI", "mongodb+srv://aamp898989:dronesurvillance@cluster0.cftmhkh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"),
        ("DATABASE_NAME", "drone_alerts_db"),
        ("ENVIRONMENT", "production"),
        ("DEBUG", "false"),
        ("HOST", "0.0.0.0"),
        ("PORT", "8080")
    ]
    
    for var, value in variables:
        print(f"   {var} = {value}")
    
    print("\n📋 Step 3: Save and Wait")
    print("   - Click Save")
    print("   - Wait 2-3 minutes for redeploy")
    print("   - Check logs for MongoDB connection")
    
    print("\n📋 Step 4: Test")
    print("   - Run: python test_railway.py")
    print("   - Should see 200 OK responses")

def show_railway_cli_alternative():
    """Show Railway CLI alternative"""
    print("\n🚀 Alternative: Railway CLI")
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

def show_expected_results():
    """Show expected results after fix"""
    print("\n🎯 Expected Results After Fix:")
    print("=" * 40)
    
    print("✅ No more PostgreSQL errors")
    print("✅ MongoDB connection successful")
    print("✅ / - Root endpoint (200 OK)")
    print("✅ /health - Health check (200 OK)")
    print("✅ /api/alerts - Get alerts (200 OK)")
    print("✅ /api/stats - Get stats (200 OK)")
    print("✅ POST /api/alerts - Create alert (200/201 OK)")
    print("✅ Database operations working")

def show_troubleshooting():
    """Show troubleshooting steps"""
    print("\n🔧 If Issues Persist:")
    print("=" * 30)
    
    print("1. Check Railway logs for:")
    print("   - MongoDB connection success")
    print("   - No more DATABASE_URL errors")
    print("   - Application startup complete")
    
    print("\n2. Verify environment variables:")
    print("   - All variables are set correctly")
    print("   - No typos in MONGODB_URI")
    print("   - Variables are saved")
    
    print("\n3. Force redeploy:")
    print("   - Go to Railway dashboard")
    print("   - Click 'Deploy' button")
    print("   - Wait for deployment to complete")

def main():
    """Main function"""
    print("🚁 Railway Quick Fix")
    print("=" * 50)
    
    # Show immediate fix
    show_immediate_fix()
    
    # Show CLI alternative
    show_railway_cli_alternative()
    
    # Show expected results
    show_expected_results()
    
    # Show troubleshooting
    show_troubleshooting()
    
    print("\n💡 Priority Actions:")
    print("=" * 30)
    print("1. 🚨 Set MONGODB_URI in Railway dashboard NOW")
    print("2. ⏰ Wait 2-3 minutes for redeploy")
    print("3. 🧪 Test with: python test_railway.py")
    print("4. 📊 Check logs for success messages")
    
    print("\n🎯 The key issue is Railway trying to use PostgreSQL")
    print("   instead of MongoDB. Setting MONGODB_URI will fix this!")

if __name__ == "__main__":
    main() 