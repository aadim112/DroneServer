import asyncio
import logging
import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

from config import Config

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db = None
        self.alerts_collection = None
        self.is_connected = False
        self.change_stream = None
        
    async def connect(self):
        """Connect to MongoDB with proper SSL configuration"""
        try:
            logger.info("Connecting to MongoDB...")
            logger.info(f"Connection string: {Config.MONGODB_URI[:50]}...")
            
            # Add SSL parameters to connection string
            connection_string = Config.MONGODB_URI
            
            # If connection string doesn't have SSL parameters, add them
            if "ssl=true" not in connection_string and "tls=true" not in connection_string:
                if "?" in connection_string:
                    connection_string += "&ssl=true&ssl_cert_reqs=CERT_NONE"
                else:
                    connection_string += "?ssl=true&ssl_cert_reqs=CERT_NONE"
            
            logger.info(f"Final connection string: {connection_string[:50]}...")
            
            # Create client with proper SSL configuration
            self.client = AsyncIOMotorClient(
                connection_string,
                serverSelectionTimeoutMS=30000,  # Increased timeout
                connectTimeoutMS=30000,          # Increased timeout
                socketTimeoutMS=30000,           # Increased timeout
                maxPoolSize=10,
                retryWrites=True,
                w="majority"
            )
            
            # Test connection
            logger.info("Testing MongoDB connection...")
            await self.client.admin.command('ping')
            logger.info("MongoDB ping successful")
            
            # Set up database and collection
            self.db = self.client[Config.DATABASE_NAME]
            self.alerts_collection = self.db[Config.ALERTS_COLLECTION]
            
            # Test database access
            logger.info(f"Testing database access: {Config.DATABASE_NAME}")
            await self.alerts_collection.count_documents({})
            logger.info("Database access successful")
            
            self.is_connected = True
            logger.info("Successfully connected to MongoDB")
            
        except ConnectionFailure as e:
            logger.error(f"MongoDB connection failure: {e}")
            self.is_connected = False
            raise
        except ServerSelectionTimeoutError as e:
            logger.error(f"MongoDB server selection timeout: {e}")
            self.is_connected = False
            raise
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            self.is_connected = False
            raise
    
    async def disconnect(self):
        """Disconnect from MongoDB"""
        try:
            if self.change_stream:
                await self.change_stream.close()
            
            if self.client:
                self.client.close()
                
            self.is_connected = False
            logger.info("Disconnected from MongoDB")
            
        except Exception as e:
            logger.error(f"Error disconnecting from MongoDB: {e}")
    
    async def create_alert(self, alert_data: Dict[str, Any]) -> str:
        """Create a new alert"""
        try:
            if not self.is_connected:
                raise Exception("Database not connected")
            
            # Generate a unique alert_id if not provided
            if 'alert_id' not in alert_data or not alert_data['alert_id']:
                import uuid
                alert_data['alert_id'] = f"alert_{uuid.uuid4().hex[:8]}"
            
            # Add timestamp if not present
            if 'timestamp' not in alert_data:
                alert_data['timestamp'] = datetime.utcnow().isoformat()
            
            # Add created_at field
            alert_data['created_at'] = datetime.utcnow()
            
            # Set default values if not present
            if 'response' not in alert_data:
                alert_data['response'] = 0
            if 'image_received' not in alert_data:
                alert_data['image_received'] = 0
            if 'status' not in alert_data:
                alert_data['status'] = 'pending'
            
            result = await self.alerts_collection.insert_one(alert_data)
            logger.info(f"Created alert with ID: {result.inserted_id}")
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"Error creating alert: {e}")
            raise
    
    async def insert_alert(self, alert_data: Dict[str, Any]) -> str:
        """Insert a new alert (alias for create_alert)"""
        return await self.create_alert(alert_data)
    
    async def update_alert(self, alert_id: str, update_data: Dict[str, Any]) -> bool:
        """Update alert with any data"""
        try:
            if not self.is_connected:
                raise Exception("Database not connected")
            
            from bson import ObjectId
            result = await self.alerts_collection.update_one(
                {'_id': ObjectId(alert_id)},
                {'$set': update_data}
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Error updating alert {alert_id}: {e}")
            raise
    
    async def get_all_alerts(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all alerts"""
        try:
            if not self.is_connected:
                raise Exception("Database not connected")
            
            cursor = self.alerts_collection.find().sort('created_at', -1).limit(limit)
            alerts = await cursor.to_list(length=limit)
            
            # Convert ObjectId to string for JSON serialization
            for alert in alerts:
                if '_id' in alert:
                    alert['id'] = str(alert['_id'])
                    del alert['_id']
            
            return alerts
            
        except Exception as e:
            logger.error(f"Error getting alerts: {e}")
            raise
    
    async def get_alert(self, alert_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific alert by ID"""
        try:
            if not self.is_connected:
                raise Exception("Database not connected")
            
            from bson import ObjectId
            alert = await self.alerts_collection.find_one({'_id': ObjectId(alert_id)})
            
            if alert:
                alert['id'] = str(alert['_id'])
                del alert['_id']
            
            return alert
            
        except Exception as e:
            logger.error(f"Error getting alert {alert_id}: {e}")
            raise
    
    async def update_alert_response(self, alert_id: str, response_data: Dict[str, Any]) -> bool:
        """Update alert response"""
        try:
            if not self.is_connected:
                raise Exception("Database not connected")
            
            from bson import ObjectId
            result = await self.alerts_collection.update_one(
                {'_id': ObjectId(alert_id)},
                {'$set': response_data}
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Error updating alert response: {e}")
            raise
    
    async def update_alert_image(self, alert_id: str, image_data: Dict[str, Any]) -> bool:
        """Update alert image"""
        try:
            if not self.is_connected:
                raise Exception("Database not connected")
            
            from bson import ObjectId
            result = await self.alerts_collection.update_one(
                {'_id': ObjectId(alert_id)},
                {'$set': image_data}
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Error updating alert image: {e}")
            raise
    
    async def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        try:
            if not self.is_connected:
                raise Exception("Database not connected")
            
            total_alerts = await self.alerts_collection.count_documents({})
            
            # Count alerts by status
            pending_alerts = await self.alerts_collection.count_documents({'rl_responsed': 0})
            responded_alerts = await self.alerts_collection.count_documents({'rl_responsed': 1})
            
            # Count unique drones
            unique_drones = await self.alerts_collection.distinct('drone_id')
            
            return {
                'total_alerts': total_alerts,
                'pending_alerts': pending_alerts,
                'responded_alerts': responded_alerts,
                'active_drones': len(unique_drones),
                'system_status': 'operational' if self.is_connected else 'disconnected',
                'database_status': 'connected' if self.is_connected else 'disconnected',
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting system stats: {e}")
            return {
                'total_alerts': 0,
                'pending_alerts': 0,
                'responded_alerts': 0,
                'active_drones': 0,
                'system_status': 'error',
                'database_status': 'error',
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }
    
    async def start_change_stream(self, callback):
        """Start MongoDB change stream to watch for alert updates"""
        try:
            if not self.is_connected:
                logger.warning("Cannot start change stream: database not connected")
                return
            
            logger.info("Starting MongoDB change stream...")
            
            # Create change stream pipeline
            pipeline = [
                {
                    '$match': {
                        'operationType': {'$in': ['insert', 'update', 'replace']}
                    }
                }
            ]
            
            self.change_stream = self.alerts_collection.watch(pipeline)
            logger.info("MongoDB change stream created successfully")
            
            # Start listening for changes
            async for change in self.change_stream:
                try:
                    await callback(change)
                except Exception as e:
                    logger.error(f"Error in change stream callback: {e}")
                    
        except Exception as e:
            logger.error(f"Error starting change stream: {e}")
            # Don't re-raise the exception to avoid blocking startup

    async def fix_database_schema(self):
        """Fix database schema issues"""
        try:
            if not self.is_connected:
                raise Exception("Database not connected")
            
            logger.info("Fixing database schema...")
            
            # Drop the problematic alert_id index if it exists
            try:
                await self.alerts_collection.drop_index("alert_id_1")
                logger.info("Dropped problematic alert_id index")
            except Exception as e:
                logger.info(f"alert_id index not found or already dropped: {e}")
            
            # Create a proper index on alert_id that allows null values
            try:
                await self.alerts_collection.create_index("alert_id", unique=True, sparse=True)
                logger.info("Created proper alert_id index with sparse option")
            except Exception as e:
                logger.info(f"alert_id index creation: {e}")
            
            # Create other useful indexes
            try:
                await self.alerts_collection.create_index("drone_id")
                await self.alerts_collection.create_index("created_at")
                await self.alerts_collection.create_index("status")
                logger.info("Created additional indexes")
            except Exception as e:
                logger.info(f"Additional index creation: {e}")
            
            logger.info("Database schema fixed successfully")
            
        except Exception as e:
            logger.error(f"Error fixing database schema: {e}")
            raise

# Create global database manager instance
db_manager = DatabaseManager() 