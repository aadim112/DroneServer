# 🚀 Deploying Drone Alert Server to Vercel

## 📋 Overview

This guide will help you deploy your FastAPI drone alert server to Vercel. Vercel is a serverless platform that's great for API deployments.

## ⚠️ Important Notes

**Vercel Limitations:**
- ❌ No WebSocket support (serverless functions can't maintain persistent connections)
- ❌ No long-running processes (change streams, background tasks)
- ✅ REST API endpoints work perfectly
- ✅ Database connections work (but are created per request)

**What Works on Vercel:**
- ✅ All REST API endpoints (`/api/alerts`, `/health`, etc.)
- ✅ Database operations (MongoDB)
- ✅ CORS and middleware
- ✅ API documentation (`/docs`)

## 🛠️ Setup Steps

### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

### Step 2: Login to Vercel

```bash
vercel login
```

### Step 3: Configure Environment Variables

Create a `.env.local` file (for local testing):

```env
MONGODB_URI=mongodb+srv://aamp898989:dronesurvillance@cluster0.cftmhkh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
DATABASE_NAME=drone_alerts_db
```

### Step 4: Deploy to Vercel

```bash
vercel
```

Or for production:

```bash
vercel --prod
```

## 📁 Project Structure for Vercel

```
Final Server/
├── main_vercel.py      # Vercel-compatible server
├── vercel.json         # Vercel configuration
├── requirements.txt    # Python dependencies
├── database.py         # Database operations
├── models.py           # Data models
├── config.py           # Configuration
└── websocket_manager.py # (Not used in Vercel)
```

## 🔧 Configuration Files

### vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "main_vercel.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main_vercel.py"
    }
  ],
  "functions": {
    "main_vercel.py": {
      "maxDuration": 30
    }
  },
  "env": {
    "PYTHONPATH": "."
  }
}
```

### requirements.txt
```txt
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
pymongo==4.6.0
python-dotenv==1.0.0
```

## 🌐 API Endpoints Available

After deployment, your API will be available at:
`https://your-project-name.vercel.app`

### Available Endpoints:
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /api/alerts` - Get all alerts
- `POST /api/alerts` - Create new alert
- `GET /api/alerts/{alert_id}` - Get specific alert
- `PUT /api/alerts/{alert_id}/response` - Update alert response
- `PUT /api/alerts/{alert_id}/image` - Update alert image
- `GET /api/stats` - System statistics
- `GET /docs` - API documentation

## 📤 How to Send Data

### Method 1: REST API (Recommended for Vercel)

```python
import requests
import json
from datetime import datetime

# Your Vercel deployment URL
base_url = "https://your-project-name.vercel.app"

# Alert data
alert_data = {
    "alert": "Intrusion Detected",
    "drone_id": "drone_001",
    "alert_location": [40.7128, -74.0060, 100.0],
    "image": None,
    "image_received": 0,
    "rl_responsed": 0,
    "score": 0.95,
    "timestamp": datetime.utcnow().isoformat()
}

# Send POST request
response = requests.post(
    f"{base_url}/api/alerts",
    json=alert_data,
    headers={"Content-Type": "application/json"}
)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

### Method 2: Using cURL

```bash
curl -X POST "https://your-project-name.vercel.app/api/alerts" \
  -H "Content-Type: application/json" \
  -d '{
    "alert": "Fire Detected",
    "drone_id": "drone_002",
    "alert_location": [40.7589, -73.9851, 50.0],
    "score": 0.88,
    "timestamp": "2025-07-27T13:15:00Z"
  }'
```

## 🔍 Testing Your Deployment

### 1. Test Health Endpoint
```bash
curl https://your-project-name.vercel.app/health
```

### 2. Test API Documentation
Visit: `https://your-project-name.vercel.app/docs`

### 3. Test Alert Creation
```bash
curl -X POST "https://your-project-name.vercel.app/api/alerts" \
  -H "Content-Type: application/json" \
  -d '{
    "alert": "Test Alert",
    "drone_id": "test_drone",
    "alert_location": [0, 0, 0],
    "score": 0.5,
    "timestamp": "2025-07-27T13:15:00Z"
  }'
```

## 🚨 Troubleshooting

### Common Issues:

1. **Database Connection Errors**
   - Check if `MONGODB_URI` is set in Vercel environment variables
   - Ensure MongoDB Atlas allows connections from Vercel IPs

2. **Import Errors**
   - Make sure all dependencies are in `requirements.txt`
   - Check that `PYTHONPATH` is set correctly

3. **Function Timeout**
   - Increase `maxDuration` in `vercel.json` if needed

### Setting Environment Variables in Vercel:

1. Go to your Vercel dashboard
2. Select your project
3. Go to Settings → Environment Variables
4. Add:
   - `MONGODB_URI` = Your MongoDB connection string
   - `DATABASE_NAME` = drone_alerts_db

## 📊 Monitoring

- **Vercel Dashboard**: Monitor function calls, errors, and performance
- **Function Logs**: View logs in Vercel dashboard
- **API Documentation**: Available at `/docs` endpoint

## 🔄 Updates

To update your deployment:

```bash
git add .
git commit -m "Update server"
vercel --prod
```

## 🎯 Benefits of Vercel Deployment

✅ **Automatic Scaling**: Handles traffic spikes automatically
✅ **Global CDN**: Fast response times worldwide
✅ **Zero Configuration**: Simple deployment process
✅ **Free Tier**: Generous free tier for development
✅ **Automatic HTTPS**: SSL certificates included
✅ **Git Integration**: Automatic deployments from Git

## 📞 Support

If you encounter issues:
1. Check Vercel function logs
2. Verify environment variables
3. Test database connectivity
4. Check API documentation at `/docs` 