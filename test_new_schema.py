from pymongo import MongoClient
from datetime import datetime
import asyncio
from database import DatabaseManager

# Example payload matching the new schema
def create_sample_alert():
    return {
        "alert": "Casualty - Person Detected",
        "drone_id": "NO DRONE",
        "alert_location": (0, 0, 0),
        "image": None,
        "image_received": 0,
        "rl_responsed": 0,
        "score": 0.95,
        "timestamp": datetime.utcnow().isoformat()
    }

async def test_new_schema():
    """Test the new database schema"""
    db_manager = DatabaseManager()
    
    try:
        # Connect to database
        await db_manager.connect()
        print("Connected to database successfully")
        
        # Insert a sample alert with new schema
        sample_alert = create_sample_alert()
        alert_id = await db_manager.insert_alert(sample_alert)
        print(f"Inserted alert with ID: {alert_id}")
        
        # Retrieve the alert
        retrieved_alert = await db_manager.get_alert(alert_id)
        if retrieved_alert:
            print("Retrieved alert:")
            print(f"  Alert: {retrieved_alert['alert']}")
            print(f"  Drone ID: {retrieved_alert['drone_id']}")
            print(f"  Location: {retrieved_alert['alert_location']}")
            print(f"  Score: {retrieved_alert['score']}")
            print(f"  Image Received: {retrieved_alert['image_received']}")
            print(f"  RL Responded: {retrieved_alert['rl_responsed']}")
            print(f"  Timestamp: {retrieved_alert['timestamp']}")
        
        # Get all alerts
        all_alerts = await db_manager.get_all_alerts(limit=5)
        print(f"\nTotal alerts in database: {len(all_alerts)}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await db_manager.disconnect()
        print("Disconnected from database")

if __name__ == "__main__":
    asyncio.run(test_new_schema()) 