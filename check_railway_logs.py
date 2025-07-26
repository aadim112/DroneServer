#!/usr/bin/env python3
"""
Check Railway Logs and Deployment Status
"""

import requests
import json
import time

def check_railway_deployment():
    """Check if Railway deployment is working"""
    print("🔍 Checking Railway deployment status...")
    
    # You'll need to replace this with your actual Railway app URL
    # Get this from your Railway dashboard
    app_url = input("Enter your Railway app URL (e.g., https://your-app.railway.app): ").strip()
    
    if not app_url:
        print("❌ No URL provided. Please get your app URL from Railway dashboard.")
        return
    
    endpoints = [
        ("Health Check", f"{app_url}/health"),
        ("Root", f"{app_url}/"),
        ("Get Alerts", f"{app_url}/api/alerts"),
        ("Stats", f"{app_url}/api/stats")
    ]
    
    print(f"\n🌐 Testing endpoints for: {app_url}")
    print("=" * 50)
    
    for name, url in endpoints:
        try:
            response = requests.get(url, timeout=10)
            print(f"✅ {name}: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Response: {json.dumps(data, indent=2)}")
            else:
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"❌ {name}: Error - {e}")
        print()

def show_railway_dashboard_instructions():
    """Show how to access Railway dashboard"""
    print("\n📋 How to Access Railway Dashboard:")
    print("=" * 40)
    print("1. Go to https://railway.app")
    print("2. Sign in with your GitHub account")
    print("3. Click on your project")
    print("4. Go to 'Deployments' tab")
    print("5. Click on the latest deployment")
    print("6. Check 'Logs' tab for real-time logs")
    print("7. Copy your app URL from 'Settings' tab")

def show_data_storage_options():
    """Show different data storage options"""
    print("\n💾 Data Storage Options:")
    print("=" * 30)
    print("1. 📊 Railway Logs - Real-time deployment logs")
    print("2. 🌐 API Endpoints - Test your deployed endpoints")
    print("3. 📝 Local Testing - Test locally before deploying")
    print("4. 🗄️  Database - Add MongoDB for persistent storage")
    print("5. 📱 Web Dashboard - Create a web interface")

if __name__ == "__main__":
    print("🚀 Railway Deployment Checker")
    print("=" * 30)
    
    show_railway_dashboard_instructions()
    
    choice = input("\nDo you want to test your deployed endpoints? (y/n): ").lower()
    if choice == 'y':
        check_railway_deployment()
    
    show_data_storage_options() 