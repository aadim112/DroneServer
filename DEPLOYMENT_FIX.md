# 🚁 Drone Server Deployment Fix Guide

## 🔍 Problem Identified

Your deployed server at `https://droneserver-production.up.railway.app` is returning **500 Internal Server Errors** because:

1. **Missing Dependencies**: `requirements.txt` was missing `pymongo` and `python-dotenv`
2. **Wrong Entry Point**: `Procfile` was pointing to a deleted file (`railway_minimal.py`)
3. **Database Connection Issues**: Server can't connect to MongoDB

## ✅ Fixes Applied

### 1. Fixed Procfile
```bash
# Changed from:
web: python railway_minimal.py

# To:
web: python main.py
```

### 2. Updated requirements.txt
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pymongo==4.6.0
python-dotenv==1.0.0
```

## 🚀 Deployment Steps

### Step 1: Commit and Push Changes
```bash
git add .
git commit -m "Fix deployment issues: update Procfile and requirements.txt"
git push origin main
```

### Step 2: Check Railway Deployment
1. Go to your Railway dashboard
2. Check the deployment logs for any errors
3. Ensure the build completes successfully

### Step 3: Verify Environment Variables
Make sure these environment variables are set in Railway:
- `MONGODB_URI` - Your MongoDB connection string
- `DATABASE_NAME` - Database name (default: drone_alerts_db)
- `PORT` - Port number (Railway sets this automatically)

### Step 4: Test the Deployment
After deployment, test with:
```bash
python test_deployed_api.py
```

## 🧪 Local Testing

Before deploying, test locally:

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start Local Server
```bash
python main.py
```

### 3. Test Local Server
```bash
python test_local_server.py
```

## 📋 API Endpoints

Your server should have these endpoints:

### REST API
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /api/alerts` - Get all alerts
- `POST /api/alerts` - Create new alert
- `GET /api/alerts/{alert_id}` - Get specific alert
- `PUT /api/alerts/{alert_id}/response` - Update alert response
- `PUT /api/alerts/{alert_id}/image` - Update alert image
- `GET /api/stats` - Get system statistics

### WebSocket Endpoints
- `WS /ws/drone/{drone_id}` - Drone WebSocket connection
- `WS /ws/application/{app_id}` - Application WebSocket connection

### Dashboard
- `GET /dashboard/` - Web dashboard
- `GET /docs` - API documentation

## 🔧 Troubleshooting

### If Still Getting 500 Errors:

1. **Check Railway Logs**
   ```bash
   # View deployment logs in Railway dashboard
   ```

2. **Test Database Connection**
   ```python
   # Add this to main.py temporarily
   import asyncio
   from database import db_manager
   
   async def test_db():
       await db_manager.connect()
       print("Database connected successfully!")
       await db_manager.disconnect()
   
   if __name__ == "__main__":
       asyncio.run(test_db())
   ```

3. **Check Environment Variables**
   - Verify `MONGODB_URI` is correct
   - Ensure MongoDB Atlas allows connections from Railway IPs

4. **Test Minimal Server**
   ```python
   # Create a minimal test server
   from fastapi import FastAPI
   
   app = FastAPI()
   
   @app.get("/")
   def read_root():
       return {"Hello": "World"}
   
   @app.get("/health")
   def health():
       return {"status": "healthy"}
   ```

## 📞 Support

If issues persist:
1. Check Railway deployment logs
2. Verify MongoDB connection string
3. Test with minimal server first
4. Check if all dependencies are installed

## 🎯 Expected Result

After fixing, your server should:
- ✅ Start without errors
- ✅ Connect to MongoDB successfully
- ✅ Respond to API requests
- ✅ Accept WebSocket connections
- ✅ Store and retrieve alert data 