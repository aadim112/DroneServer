#!/usr/bin/env python3
"""
System Test Script
Tests the drone alert management system components
"""

import asyncio
import aiohttp
import json
import sys
from datetime import datetime
from typing import Dict, Any

# Test configuration
SERVER_URL = "http://localhost:8000"
TEST_ALERT = {
    "alert_type": "intrusion",
    "score": 0.85,
    "location": {"lat": 40.7128, "lng": -74.0060},
    "drone_id": "test_drone_001",
    "description": "Test intrusion alert"
}

async def test_health_endpoint():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{SERVER_URL}/health") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Health check passed: {data['status']}")
                    return True
                else:
                    print(f"❌ Health check failed: {response.status}")
                    return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

async def test_create_alert():
    """Test creating an alert via REST API"""
    print("🔍 Testing alert creation...")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{SERVER_URL}/api/alerts",
                json=TEST_ALERT
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Alert created: {data['alert_id']}")
                    return data['alert_id']
                else:
                    print(f"❌ Alert creation failed: {response.status}")
                    return None
    except Exception as e:
        print(f"❌ Alert creation error: {e}")
        return None

async def test_get_alerts():
    """Test getting alerts"""
    print("🔍 Testing get alerts...")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{SERVER_URL}/api/alerts") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Retrieved {data['count']} alerts")
                    return data['alerts']
                else:
                    print(f"❌ Get alerts failed: {response.status}")
                    return []
    except Exception as e:
        print(f"❌ Get alerts error: {e}")
        return []

async def test_update_alert_response(alert_id: str):
    """Test updating alert response"""
    print("🔍 Testing alert response update...")
    try:
        update_data = {
            "alert_id": alert_id,
            "actions": ["test_action_1", "test_action_2"],
            "response": 1
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.put(
                f"{SERVER_URL}/api/alerts/{alert_id}/response",
                json=update_data
            ) as response:
                if response.status == 200:
                    print(f"✅ Alert response updated successfully")
                    return True
                else:
                    print(f"❌ Alert response update failed: {response.status}")
                    return False
    except Exception as e:
        print(f"❌ Alert response update error: {e}")
        return False

async def test_update_alert_image(alert_id: str):
    """Test updating alert image"""
    print("🔍 Testing alert image update...")
    try:
        update_data = {
            "alert_id": alert_id,
            "image_url": "http://localhost:8000/uploads/test_image.jpg",
            "image_received": 1
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.put(
                f"{SERVER_URL}/api/alerts/{alert_id}/image",
                json=update_data
            ) as response:
                if response.status == 200:
                    print(f"✅ Alert image updated successfully")
                    return True
                else:
                    print(f"❌ Alert image update failed: {response.status}")
                    return False
    except Exception as e:
        print(f"❌ Alert image update error: {e}")
        return False

async def test_get_stats():
    """Test getting system stats"""
    print("🔍 Testing system stats...")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{SERVER_URL}/api/stats") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ System stats retrieved")
                    print(f"   - Database connected: {data['database_connected']}")
                    print(f"   - Total connections: {data['websocket_stats']['total_connections']}")
                    return True
                else:
                    print(f"❌ Get stats failed: {response.status}")
                    return False
    except Exception as e:
        print(f"❌ Get stats error: {e}")
        return False

async def run_all_tests():
    """Run all system tests"""
    print("🚀 Starting Drone Alert Management System Tests")
    print("=" * 50)
    
    # Test health endpoint
    if not await test_health_endpoint():
        print("❌ Health check failed. Is the server running?")
        return False
    
    # Test creating an alert
    alert_id = await test_create_alert()
    if not alert_id:
        print("❌ Alert creation failed")
        return False
    
    # Test getting alerts
    alerts = await test_get_alerts()
    if not alerts:
        print("❌ Get alerts failed")
        return False
    
    # Test updating alert response
    if not await test_update_alert_response(alert_id):
        print("❌ Alert response update failed")
        return False
    
    # Test updating alert image
    if not await test_update_alert_image(alert_id):
        print("❌ Alert image update failed")
        return False
    
    # Test getting stats
    if not await test_get_stats():
        print("❌ Get stats failed")
        return False
    
    print("\n" + "=" * 50)
    print("✅ All tests passed! System is working correctly.")
    print("🎉 You can now:")
    print("   - Start the server: python run_server.py")
    print("   - Run drone client: python examples/drone_client.py")
    print("   - Run app client: python examples/application_client.py")
    print("   - View dashboard: http://localhost:8000/dashboard/")
    
    return True

def main():
    """Main function"""
    try:
        success = asyncio.run(run_all_tests())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Test error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 