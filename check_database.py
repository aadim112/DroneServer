#!/usr/bin/env python3
"""
Check Database for Alert Images
Simple script to check if alert images are being saved to the database
"""

import requests
import json
from datetime import datetime

# Configuration
SERVER_URL = "https://web-production-190fc.up.railway.app"

def check_alert_images():
    """Check for alert images in the database"""
    
    print("🔍 Checking Database for Alert Images")
    print("=" * 50)
    
    try:
        # Get all alert images
        response = requests.get(f"{SERVER_URL}/api/alert-images?limit=10")
        
        if response.status_code == 200:
            data = response.json()
            alert_images = data.get("alert_images", [])
            
            print(f"✅ Found {len(alert_images)} alert images in database")
            print()
            
            for i, img in enumerate(alert_images, 1):
                print(f"📸 Alert Image #{i}:")
                print(f"   - ID: {img.get('id', 'N/A')}")
                print(f"   - Name: {img.get('name', 'N/A')}")
                print(f"   - Drone ID: {img.get('drone_id', 'N/A')}")
                print(f"   - Found: {img.get('found', 'N/A')}")
                print(f"   - Location: {img.get('location', 'N/A')}")
                print(f"   - Timestamp: {img.get('timestamp', 'N/A')}")
                print(f"   - Has actual_image: {'Yes' if img.get('actual_image') else 'No'}")
                print(f"   - Has matched_frame: {'Yes' if img.get('matched_frame') else 'No'}")
                print()
        else:
            print(f"❌ Failed to get alert images: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error checking database: {e}")

def check_system_stats():
    """Check system statistics"""
    
    print("📊 System Statistics")
    print("=" * 30)
    
    try:
        response = requests.get(f"{SERVER_URL}/api/stats")
        
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Database connected: {stats.get('database_connected', 'N/A')}")
            print(f"✅ Total alerts: {stats.get('total_alerts', 'N/A')}")
            print(f"✅ Total alert images: {stats.get('total_alert_images', 'N/A')}")
            print(f"✅ WebSocket connections: {stats.get('websocket_stats', 'N/A')}")
        else:
            print(f"❌ Failed to get stats: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error getting stats: {e}")

def check_health():
    """Check server health"""
    
    print("🏥 Server Health Check")
    print("=" * 30)
    
    try:
        response = requests.get(f"{SERVER_URL}/health")
        
        if response.status_code == 200:
            health = response.json()
            print(f"✅ Status: {health.get('status', 'N/A')}")
            print(f"✅ Database connected: {health.get('database_connected', 'N/A')}")
            print(f"✅ WebSocket stats: {health.get('websocket_stats', 'N/A')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error checking health: {e}")

def main():
    """Main function"""
    print("🚁 Database Checker")
    print("=" * 50)
    
    # Check server health first
    check_health()
    print()
    
    # Check system stats
    check_system_stats()
    print()
    
    # Check alert images
    check_alert_images()
    
    print("✅ Database check completed!")

if __name__ == "__main__":
    main() 