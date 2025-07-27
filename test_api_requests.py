#!/usr/bin/env python3
"""
Essential API test script for Drone Alert Management System
"""

import requests
import json

def test_essential_api():
    """Test essential API endpoints"""
    base_url = "http://localhost:8000"
    
    print("🚀 Essential API Testing")
    print("=" * 40)
    
    # Test 1: Health Check
    print("\n1️⃣ Health Check")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Server healthy - Database: {data.get('database_connected', False)}")
        else:
            print(f"   ❌ Health check failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Create Alert
    print("\n2️⃣ Create Alert")
    try:
        test_alert = {
            "alert": "Test intrusion detection",
            "drone_id": "test_drone_001",
            "alert_location": [40.7128, -74.0060, 0.0],
            "score": 0.85,
            "timestamp": "2025-07-27T17:50:00Z",
            "image": None,
            "image_received": 0,
            "rl_responsed": 0
        }
        
        response = requests.post(
            f"{base_url}/api/alerts",
            headers={"Content-Type": "application/json"},
            json=test_alert
        )
        if response.status_code == 200:
            data = response.json()
            alert_id = data.get('alert_id')
            print(f"   ✅ Alert created - ID: {alert_id}")
            
            # Test 3: Update Alert Response
            print("\n3️⃣ Update Alert Response")
            update_data = {"alert_id": alert_id, "rl_responsed": 1}
            response = requests.put(
                f"{base_url}/api/alerts/{alert_id}/response",
                headers={"Content-Type": "application/json"},
                json=update_data
            )
            if response.status_code == 200:
                print(f"   ✅ Alert response updated")
            else:
                print(f"   ❌ Failed to update response")
                
            # Test 4: Get All Alerts
            print("\n4️⃣ Get All Alerts")
            response = requests.get(f"{base_url}/api/alerts")
            if response.status_code == 200:
                data = response.json()
                alerts = data.get('alerts', [])
                print(f"   ✅ Retrieved {len(alerts)} alerts")
            else:
                print(f"   ❌ Failed to get alerts")
                
        else:
            print(f"   ❌ Failed to create alert")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 40)
    print("🎯 Essential API Testing Complete!")

if __name__ == "__main__":
    test_essential_api() 