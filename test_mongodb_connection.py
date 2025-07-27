import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_mongodb_connection():
    """Test MongoDB connection with detailed error reporting"""
    
    # Get connection string from environment
    mongodb_uri = os.getenv('MONGODB_URI', 'mongodb+srv://aamp898989:dronesurvillance@cluster0.cftmhkh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
    database_name = os.getenv('DATABASE_NAME', 'drone_alerts_db')
    
    print(f"🔍 Testing MongoDB Connection...")
    print(f"📊 Database: {database_name}")
    print(f"🔗 URI: {mongodb_uri[:50]}...")
    
    try:
        # Test 1: Basic connection
        print("\n1️⃣ Testing basic connection...")
        client = AsyncIOMotorClient(
            mongodb_uri,
            serverSelectionTimeoutMS=10000,
            connectTimeoutMS=10000,
            socketTimeoutMS=10000,
            maxPoolSize=10,
            retryWrites=True,
            w="majority"
        )
        
        # Test 2: Ping the database
        print("2️⃣ Testing ping...")
        await client.admin.command('ping')
        print("✅ Ping successful!")
        
        # Test 3: Access the database
        print("3️⃣ Testing database access...")
        db = client[database_name]
        
        # Test 4: List collections
        print("4️⃣ Testing collection access...")
        collections = await db.list_collection_names()
        print(f"✅ Found collections: {collections}")
        
        # Test 5: Test alerts collection
        print("5️⃣ Testing alerts collection...")
        alerts_collection = db['alerts']
        count = await alerts_collection.count_documents({})
        print(f"✅ Alerts collection accessible. Document count: {count}")
        
        # Test 6: Test insert operation
        print("6️⃣ Testing insert operation...")
        test_doc = {
            "test": True,
            "timestamp": "2025-07-27T10:15:00Z",
            "message": "Connection test"
        }
        result = await alerts_collection.insert_one(test_doc)
        print(f"✅ Insert successful! ID: {result.inserted_id}")
        
        # Test 7: Test delete operation
        print("7️⃣ Cleaning up test document...")
        await alerts_collection.delete_one({"_id": result.inserted_id})
        print("✅ Cleanup successful!")
        
        client.close()
        print("\n🎉 All MongoDB tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ MongoDB connection failed: {e}")
        print(f"🔍 Error type: {type(e).__name__}")
        
        # Provide specific troubleshooting steps
        if "SSL" in str(e) or "TLS" in str(e):
            print("\n💡 SSL/TLS Issue detected!")
            print("   Try adding these parameters to your connection string:")
            print("   ?ssl=true&ssl_cert_reqs=CERT_NONE")
        elif "timeout" in str(e).lower():
            print("\n💡 Timeout Issue detected!")
            print("   Check your network connection and MongoDB Atlas settings")
        elif "authentication" in str(e).lower():
            print("\n💡 Authentication Issue detected!")
            print("   Check your username/password in the connection string")
        elif "dns" in str(e).lower():
            print("\n💡 DNS Issue detected!")
            print("   Check your internet connection and DNS settings")
        
        return False

async def test_environment_variables():
    """Test if environment variables are set correctly"""
    print("\n🔍 Checking Environment Variables...")
    
    required_vars = ['MONGODB_URI', 'DATABASE_NAME']
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {value[:30]}..." if len(value) > 30 else f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Not set")

if __name__ == "__main__":
    print("🚀 MongoDB Connection Diagnostic Tool")
    print("=" * 50)
    
    # Test environment variables
    asyncio.run(test_environment_variables())
    
    # Test MongoDB connection
    success = asyncio.run(test_mongodb_connection())
    
    if success:
        print("\n🎯 RECOMMENDATION: Database connection works locally!")
        print("   The issue might be in Railway's environment variables.")
    else:
        print("\n🎯 RECOMMENDATION: Check your MongoDB connection string and network.") 