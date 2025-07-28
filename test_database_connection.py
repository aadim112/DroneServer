import asyncio
import json
from datetime import datetime
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import db_manager
from config import Config

async def test_database_connection():
    """Test database connection and alert insertion"""
    print("Testing database connection...")
    
    try:
        # Connect to database
        await db_manager.connect()
        print("✅ Database connected successfully")
        
        # Test alert insertion
        test_alert = {
            "alert": "Database Test Alert",
            "alert_location": [0.0, 0.0, 0.0],
            "timestamp": datetime.utcnow().isoformat(),
            "alert_type": "test",
            "score": 99.0,
            "drone_id": "test_drone_001"
        }
        
        print(f"📤 Inserting test alert: {json.dumps(test_alert, indent=2)}")
        alert_id = await db_manager.insert_alert(test_alert)
        print(f"✅ Alert inserted with ID: {alert_id}")
        
        # Test retrieving the alert
        retrieved_alert = await db_manager.get_alert(alert_id)
        if retrieved_alert:
            print(f"✅ Alert retrieved successfully: {json.dumps(retrieved_alert, indent=2)}")
        else:
            print("❌ Failed to retrieve alert")
        
        # Test getting all alerts
        all_alerts = await db_manager.get_all_alerts(limit=5)
        print(f"✅ Retrieved {len(all_alerts)} alerts from database")
        
        # Test system stats
        stats = await db_manager.get_system_stats()
        print(f"✅ System stats: {json.dumps(stats, indent=2)}")
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await db_manager.disconnect()
        print("🔌 Database disconnected")

if __name__ == "__main__":
    asyncio.run(test_database_connection()) 