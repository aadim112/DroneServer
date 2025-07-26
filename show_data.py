#!/usr/bin/env python3
"""
Show Current Database Data
"""

import asyncio
import aiohttp
import json
from datetime import datetime

async def show_alerts():
    """Show all alerts in the database"""
    try:
        async with aiohttp.ClientSession() as session:
            # Get all alerts
            async with session.get("http://localhost:8000/api/alerts") as response:
                if response.status == 200:
                    data = await response.json()
                    alerts = data['alerts']
                    
                    print(f"🚁 Drone Alert Management System - Database Status")
                    print("=" * 60)
                    print(f"📊 Total Alerts: {data['count']}")
                    print(f"🕒 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    print("=" * 60)
                    
                    if not alerts:
                        print("📭 No alerts found in database")
                        return
                    
                    for i, alert in enumerate(alerts, 1):
                        print(f"\n🔔 Alert #{i}")
                        print(f"   ID: {alert.get('alert_id', 'N/A')}")
                        print(f"   Type: {alert.get('alert_type', 'N/A').upper()}")
                        print(f"   Score: {alert.get('score', 0):.2f}")
                        print(f"   Drone: {alert.get('drone_id', 'N/A')}")
                        print(f"   Status: {alert.get('status', 'N/A')}")
                        print(f"   Response: {'✅' if alert.get('response') else '❌'}")
                        print(f"   Image: {'✅' if alert.get('image_received') else '❌'}")
                        
                        if alert.get('location'):
                            loc = alert['location']
                            print(f"   Location: {loc.get('lat', 0):.4f}, {loc.get('lng', 0):.4f}")
                        
                        if alert.get('description'):
                            print(f"   Description: {alert['description']}")
                        
                        if alert.get('actions'):
                            print(f"   Actions: {', '.join(alert['actions'])}")
                        
                        if alert.get('timestamp'):
                            try:
                                ts = datetime.fromisoformat(alert['timestamp'].replace('Z', '+00:00'))
                                print(f"   Time: {ts.strftime('%Y-%m-%d %H:%M:%S')}")
                            except:
                                print(f"   Time: {alert['timestamp']}")
                        
                        print("-" * 40)
                    
                else:
                    print(f"❌ Failed to get alerts: {response.status}")
                    
    except Exception as e:
        print(f"❌ Error: {e}")

async def show_stats():
    """Show system statistics"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:8000/api/stats") as response:
                if response.status == 200:
                    data = await response.json()
                    stats = data['websocket_stats']
                    
                    print(f"\n📈 System Statistics")
                    print("=" * 30)
                    print(f"Database Connected: {'✅' if data['database_connected'] else '❌'}")
                    print(f"Total Connections: {stats['total_connections']}")
                    print(f"Drone Connections: {stats['drone_connections']}")
                    print(f"App Connections: {stats['application_connections']}")
                    print(f"Active Alerts: {stats['active_alerts']}")
                    
                else:
                    print(f"❌ Failed to get stats: {response.status}")
                    
    except Exception as e:
        print(f"❌ Error getting stats: {e}")

async def main():
    """Main function"""
    await show_alerts()
    await show_stats()
    
    print(f"\n🌐 Access Points:")
    print(f"   Dashboard: http://localhost:8000/dashboard/")
    print(f"   API Docs: http://localhost:8000/docs")
    print(f"   Health: http://localhost:8000/health")

if __name__ == "__main__":
    asyncio.run(main()) 