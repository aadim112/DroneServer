import asyncio
import logging
from typing import Optional, Callable, Dict, Any
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from bson import ObjectId
from bson.json_util import dumps, loads
import json
from datetime import datetime
from config import Config

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.client: Optional[MongoClient] = None
        self.db: Optional[Database] = None
        self.alerts_collection: Optional[Collection] = None
        self.change_stream = None
        self.is_connected = False
        
    async def connect(self):
        """Connect to MongoDB and initialize collections"""
        try:
            self.client = MongoClient(
                Config.MONGODB_URI,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000
            )
            
            # Test connection
            self.client.admin.command('ping')
            
            self.db = self.client[Config.DATABASE_NAME]
            self.alerts_collection = self.db[Config.ALERTS_COLLECTION]
            
            # Create indexes for better performance
            await self._create_indexes()
            
            self.is_connected = True
            logger.info("Successfully connected to MongoDB")
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    async def _create_indexes(self):
        """Create necessary indexes for the alerts collection"""
        try:
            # Index on timestamp for time-based queries
            self.alerts_collection.create_index("timestamp")
            
            # Index on drone_id for drone-specific queries
            self.alerts_collection.create_index("drone_id")
            
            # Index on score for confidence-based queries
            self.alerts_collection.create_index("score")
            
            # Index on rl_responsed for response status queries
            self.alerts_collection.create_index("rl_responsed")
            
            # Index on image_received for image status queries
            self.alerts_collection.create_index("image_received")
            
            logger.info("Database indexes created successfully")
        except Exception as e:
            logger.error(f"Error creating indexes: {e}")
    
    async def disconnect(self):
        """Disconnect from MongoDB"""
        if self.change_stream:
            self.change_stream.close()
        
        if self.client:
            self.client.close()
            self.is_connected = False
            logger.info("Disconnected from MongoDB")
    
    async def insert_alert(self, alert_data: Dict[str, Any]) -> str:
        """Insert a new alert into the database"""
        try:
            # Generate _id if not provided
            if '_id' not in alert_data:
                alert_data['_id'] = str(ObjectId())
            
            # Ensure timestamp is present
            if 'timestamp' not in alert_data:
                alert_data['timestamp'] = datetime.utcnow().isoformat()
            
            result = self.alerts_collection.insert_one(alert_data)
            logger.info(f"Alert inserted with ID: {alert_data['_id']}")
            return alert_data['_id']
            
        except Exception as e:
            logger.error(f"Error inserting alert: {e}")
            raise
    
    async def update_alert(self, alert_id: str, update_data: Dict[str, Any]) -> bool:
        """Update an existing alert"""
        try:
            # Remove _id from update data to avoid conflicts
            update_data.pop('_id', None)
            
            result = self.alerts_collection.update_one(
                {"_id": alert_id},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                logger.info(f"Alert {alert_id} updated successfully")
                return True
            else:
                logger.warning(f"Alert {alert_id} not found for update")
                return False
                
        except Exception as e:
            logger.error(f"Error updating alert {alert_id}: {e}")
            raise
    
    async def get_alert(self, alert_id: str) -> Optional[Dict[str, Any]]:
        """Get an alert by ID"""
        try:
            alert = self.alerts_collection.find_one({"_id": alert_id})
            if alert:
                # Convert ObjectId to string for JSON serialization
                alert['_id'] = str(alert['_id'])
                return alert
            return None
            
        except Exception as e:
            logger.error(f"Error getting alert {alert_id}: {e}")
            raise
    
    async def get_all_alerts(self, limit: int = 100) -> list:
        """Get all alerts with optional limit"""
        try:
            alerts = list(self.alerts_collection.find().sort("timestamp", -1).limit(limit))
            
            # Convert ObjectIds to strings
            for alert in alerts:
                alert['_id'] = str(alert['_id'])
            
            return alerts
            
        except Exception as e:
            logger.error(f"Error getting alerts: {e}")
            raise
    
    async def start_change_stream(self, callback: Callable[[Dict[str, Any]], None]):
        """Start MongoDB Change Stream to watch for alert changes"""
        try:
            # Check if we're running on a replica set
            try:
                # Create change stream cursor to watch for inserts and updates
                self.change_stream = self.alerts_collection.watch(
                    [
                        {'$match': {
                            '$or': [
                                {'operationType': 'insert'},
                                {'operationType': 'update'},
                                {'operationType': 'replace'}
                            ]
                        }}
                    ],
                    full_document='updateLookup'
                )
                
                logger.info("Change stream started successfully")
                
                # Process change stream events
                async def process_changes():
                    try:
                        for change in self.change_stream:
                            await self._handle_change_event(change, callback)
                    except Exception as e:
                        logger.error(f"Error in change stream: {e}")
                        # Attempt to restart change stream
                        await asyncio.sleep(5)
                        await self.start_change_stream(callback)
                
                # Start processing in background
                asyncio.create_task(process_changes())
                
            except Exception as e:
                if "replica sets" in str(e).lower():
                    logger.warning("Change streams require replica sets. Running in polling mode instead.")
                    # Fall back to polling mode
                    await self._start_polling_mode(callback)
                else:
                    raise
                    
        except Exception as e:
            logger.error(f"Error starting change stream: {e}")
            raise
    
    async def _start_polling_mode(self, callback: Callable[[Dict[str, Any]], None]):
        """Fallback polling mode when change streams are not available"""
        logger.info("Starting polling mode for alert updates")
        
        async def poll_for_changes():
            last_check = datetime.utcnow()
            
            while True:
                try:
                    # Check for new or updated alerts since last check
                    recent_alerts = self.alerts_collection.find({
                        "timestamp": {"$gte": last_check}
                    }).sort("timestamp", -1)
                    
                    for alert in recent_alerts:
                        # Convert ObjectId to string
                        alert['_id'] = str(alert['_id'])
                        
                        # Create change event
                        change_event = {
                            'operation_type': 'update',
                            'alert': alert,
                            'timestamp': datetime.utcnow().isoformat()
                        }
                        
                        # Call the callback
                        callback(change_event)
                    
                    last_check = datetime.utcnow()
                    await asyncio.sleep(2)  # Poll every 2 seconds
                    
                except Exception as e:
                    logger.error(f"Error in polling mode: {e}")
                    await asyncio.sleep(5)
        
        # Start polling in background
        asyncio.create_task(poll_for_changes())
    
    async def _handle_change_event(self, change: Dict[str, Any], callback: Callable[[Dict[str, Any]], None]):
        """Handle individual change stream events"""
        try:
            operation_type = change.get('operationType')
            
            if operation_type in ['insert', 'update', 'replace']:
                # Get the full document
                full_document = change.get('fullDocument')
                
                if full_document:
                    # Convert ObjectId to string for JSON serialization
                    full_document['_id'] = str(full_document['_id'])
                    
                    # Create change event data
                    change_event = {
                        'operation_type': operation_type,
                        'alert': full_document,
                        'timestamp': datetime.utcnow().isoformat()
                    }
                    
                    # Call the callback with the change event
                    callback(change_event)
                    
                    logger.info(f"Change stream event processed: {operation_type} for alert {full_document.get('_id')}")
            
        except Exception as e:
            logger.error(f"Error handling change event: {e}")
    
    def serialize_alert(self, alert: Dict[str, Any]) -> str:
        """Serialize alert document to JSON string"""
        try:
            return dumps(alert)
        except Exception as e:
            logger.error(f"Error serializing alert: {e}")
            raise

# Global database manager instance
db_manager = DatabaseManager() 