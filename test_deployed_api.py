#!/usr/bin/env python3
"""
Test Deployed API
Replace YOUR_APP_URL with your actual deployed URL
"""

import asyncio
import aiohttp
import json
from datetime import datetime

# Replace with your actual deployed URL
DEPLOYED_URL = "https://your-app-name.railway.app"  # Change this!

async def test_deployed_api():
    """Test the deployed API"""
    print(f"🚀 Testing Deployed API: {DEPLOYED_URL}")
    print("=" * 60)
    
    try:
        async with aiohttp.ClientSession() as session:
            
            # Test 1: Health Check
            print("1. Testing Health Check...")
            async with session.get(f"{DEPLOYED_URL}/health") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Health Check: {data['status']}")
                    print(f"   Environment: {data.get('environment', 'N/A')}")
                    print(f"   Database: {'✅' if data['database_connected'] else '❌'}")
                else:
                    print(f"❌ Health Check Failed: {response.status}")
                    return
            
            # Test 2: Get Alerts
            print("\n2. Testing Get Alerts...")
            async with session.get(f"{DEPLOYED_URL}/api/alerts") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Get Alerts: {data['count']} alerts found")
                else:
                    print(f"❌ Get Alerts Failed: {response.status}")
            
            # Test 3: Create Alert
            print("\n3. Testing Create Alert...")
            test_alert = {
                "alert_type": "intrusion",
                "score": 0.85,
                "location": {"lat": 40.7128, "lng": -74.0060},
                "drone_id": "deployed_test_drone",
                "description": "Test alert from deployed API"
            }
            
            async with session.post(
                f"{DEPLOYED_URL}/api/alerts",
                json=test_alert
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    alert_id = data['alert_id']
                    print(f"✅ Create Alert: {alert_id}")
                    
                    # Test 4: Update Alert Response
                    print("\n4. Testing Update Alert Response...")
                    update_data = {
                        "alert_id": alert_id,
                        "actions": ["deployed_action_1", "deployed_action_2"],
                        "response": 1
                    }
                    
                    async with session.put(
                        f"{DEPLOYED_URL}/api/alerts/{alert_id}/response",
                        json=update_data
                    ) as update_response:
                        if update_response.status == 200:
                            print("✅ Update Alert Response: Success")
                        else:
                            print(f"❌ Update Alert Response Failed: {update_response.status}")
                    
                    # Test 5: Update Alert Image
                    print("\n5. Testing Update Alert Image...")
                    image_data = {
                        "alert_id": alert_id,
                        "image_url": f"{DEPLOYED_URL}/uploads/test_image.jpg",
                        "image_received": 1
                    }
                    
                    async with session.put(
                        f"{DEPLOYED_URL}/api/alerts/{alert_id}/image",
                        json=image_data
                    ) as image_response:
                        if image_response.status == 200:
                            print("✅ Update Alert Image: Success")
                        else:
                            print(f"❌ Update Alert Image Failed: {image_response.status}")
                    
                else:
                    print(f"❌ Create Alert Failed: {response.status}")
            
            # Test 6: Get Stats
            print("\n6. Testing Get Stats...")
            async with session.get(f"{DEPLOYED_URL}/api/stats") as response:
                if response.status == 200:
                    data = await response.json()
                    stats = data['websocket_stats']
                    print(f"✅ Get Stats: {stats['total_connections']} connections")
                    print(f"   Environment: {data.get('environment', 'N/A')}")
                else:
                    print(f"❌ Get Stats Failed: {response.status}")
            
            print("\n" + "=" * 60)
            print("🎉 All tests completed!")
            print(f"🌐 Your API is live at: {DEPLOYED_URL}")
            print(f"📊 Dashboard: {DEPLOYED_URL}/dashboard/")
            print(f"📚 API Docs: {DEPLOYED_URL}/docs")
            
    except Exception as e:
        print(f"❌ Error testing deployed API: {e}")

if __name__ == "__main__":
    print("⚠️  IMPORTANT: Update DEPLOYED_URL in this script with your actual deployed URL!")
    print("Example: DEPLOYED_URL = 'https://my-drone-app.railway.app'")
    print()
    
    # Uncomment the line below after updating the URL
    # asyncio.run(test_deployed_api()) 