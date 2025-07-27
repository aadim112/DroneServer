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
            
            # Add SSL parameters to connection string
            connection_string = Config.MONGODB_URI
            
            # If connection string doesn't have SSL parameters, add them
            if "ssl=true" not in connection_string and "tls=true" not in connection_string:
                if "?" in connection_string:
                    connection_string += "&ssl=true&ssl_cert_reqs=CERT_NONE"
                else:
                    connection_string += "?ssl=true&ssl_cert_reqs=CERT_NONE"
            
            # Create client with proper SSL configuration
            self.client = AsyncIOMotorClient(
                connection_string,
                serverSelectionTimeoutMS=10000,
                connectTimeoutMS=10000,
                socketTimeoutMS=10000,
                maxPoolSize=10,
                retryWrites=True,
                w="majority"
            )
            
            # Test connection
            await self.client.admin.command('ping')
            
            # Set up database and collection
            self.db = self.client[Config.DATABASE_NAME]
            self.alerts_collection = self.db[Config.ALERTS_COLLECTION]
            
            self.is_connected = True
            logger.info("Successfully connected to MongoDB")
            
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
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
            
            # Add timestamp if not present
            if 'timestamp' not in alert_data:
                alert_data['timestamp'] = datetime.utcnow().isoformat()
            
            # Add created_at field
            alert_data['created_at'] = datetime.utcnow()
            
            result = await self.alerts_collection.insert_one(alert_data)
            logger.info(f"Created alert with ID: {result.inserted_id}")
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"Error creating alert: {e}")
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
            
            # Start listening for changes
            async for change in self.change_stream:
                try:
                    await callback(change)
                except Exception as e:
                    logger.error(f"Error in change stream callback: {e}")
                    
        except Exception as e:
            logger.error(f"Error starting change stream: {e}")

# Create global database manager instance
db_manager = DatabaseManager() 