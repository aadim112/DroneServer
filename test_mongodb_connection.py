#!/usr/bin/env python3
"""
Essential MongoDB connection test
"""

import asyncio
import logging
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from database import DatabaseManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_mongodb_connection():
    """Test MongoDB connection"""
    print("🔍 Testing MongoDB Connection")
    print("=" * 40)
    
    db_manager = DatabaseManager()
    
    try:
        await db_manager.connect()
        
        if db_manager.is_connected:
            print("✅ MongoDB connection successful!")
            
            # Test basic operation
            test_alert = {
                "alert": "Connection test",
                "drone_id": "test_drone",
                "alert_location": [0, 0, 0],
                "score": 0.5,
                "timestamp": "2025-07-27T17:50:00Z"
            }
            
            alert_id = await db_manager.insert_alert(test_alert)
            print(f"✅ Test alert created: {alert_id}")
            
            # Cleanup
            from bson import ObjectId
            await db_manager.alerts_collection.delete_one({"_id": ObjectId(alert_id)})
            print("✅ Test cleanup completed")
            
        else:
            print("❌ MongoDB connection failed!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        if db_manager.is_connected:
            await db_manager.disconnect()

if __name__ == "__main__":
    asyncio.run(test_mongodb_connection()) 