# 🚀 Fresh Railway Deployment Guide

## 🗑️ Step 1: Delete Current Project

1. Go to https://railway.app/dashboard
2. Select your current project
3. Go to **Settings** tab
4. Scroll down to **Danger Zone**
5. Click **Delete Project**
6. Confirm deletion

## 🆕 Step 2: Create New Project

1. Click **New Project**
2. Choose **Deploy from GitHub repo**
3. Select: `aadim112/DroneServer`
4. **Project Name**: `drone-server-fresh`
5. **Branch**: `main`
6. Click **Deploy**

## ⚙️ Step 3: Configure Environment Variables

Once the project is created, go to **Variables** tab and add:

```
MONGODB_URI=mongodb+srv://aamp898989:dronesurvillance@cluster0.cftmhkh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
DATABASE_NAME=drone_alerts_db
ENVIRONMENT=production
DEBUG=false
HOST=0.0.0.0
PORT=8080
```

## ⏰ Step 4: Wait for Deployment

1. Railway will automatically deploy
2. Wait 3-5 minutes for deployment
3. Check logs for any errors

## 🧪 Step 5: Test Deployment

After deployment, test with:
```bash
python test_railway.py
```

## ✅ Expected Results

- ✅ **No SQLAlchemy errors**
- ✅ **MongoDB connection successful**
- ✅ **Health check working (200 OK)**
- ✅ **All API endpoints working**
- ✅ **Database operations working**

## 🔧 Troubleshooting

If healthcheck still fails:
1. Check Railway logs for errors
2. Verify environment variables are set correctly
3. Wait longer for deployment (up to 5 minutes)
4. Check if MongoDB connection is successful

## 📋 Key Points

- **Fresh start** = No cached old code
- **Clean environment** = No conflicting variables
- **Correct configuration** = MongoDB only, no PostgreSQL
- **Proper healthcheck** = 120 second timeout 