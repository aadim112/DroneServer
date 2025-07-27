#!/usr/bin/env python3
"""
Disable PostgreSQL and ensure MongoDB is used
"""

import os
import sys

def check_environment():
    """Check current environment variables"""
    print("🔍 Checking Environment Variables")
    print("=" * 50)
    
    # Check for PostgreSQL-related variables
    postgres_vars = ["DATABASE_URL", "POSTGRES_URL", "POSTGRES_DB", "POSTGRES_USER", "POSTGRES_PASSWORD"]
    mongodb_vars = ["MONGODB_URI", "DATABASE_NAME"]
    
    print("\n📋 PostgreSQL Variables (should be empty or MongoDB):")
    for var in postgres_vars:
        value = os.getenv(var, "NOT_SET")
        print(f"   {var}: {value}")
    
    print("\n📋 MongoDB Variables (should be set):")
    for var in mongodb_vars:
        value = os.getenv(var, "NOT_SET")
        print(f"   {var}: {value}")
    
    # Check if DATABASE_URL is pointing to MongoDB
    database_url = os.getenv("DATABASE_URL", "")
    if database_url and "mongodb" in database_url.lower():
        print("\n✅ DATABASE_URL is correctly pointing to MongoDB")
    elif database_url:
        print(f"\n❌ DATABASE_URL is pointing to: {database_url}")
        print("   This should be a MongoDB connection string")
    else:
        print("\n⚠️ DATABASE_URL is not set")

def show_railway_fix():
    """Show how to fix Railway configuration"""
    print("\n🔧 Railway Fix Steps:")
    print("=" * 30)
    
    print("\n📋 Step 1: Remove PostgreSQL Variables")
    print("   In Railway dashboard, remove these variables if they exist:")
    print("   - POSTGRES_URL")
    print("   - POSTGRES_DB")
    print("   - POSTGRES_USER")
    print("   - POSTGRES_PASSWORD")
    
    print("\n📋 Step 2: Set MongoDB Variables")
    print("   Ensure these variables are set:")
    print("   MONGODB_URI=mongodb+srv://aamp898989:dronesurvillance@cluster0.cftmhkh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    print("   DATABASE_NAME=drone_alerts_db")
    print("   DATABASE_URL=mongodb+srv://aamp898989:dronesurvillance@cluster0.cftmhkh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    
    print("\n📋 Step 3: Force Redeploy")
    print("   - Go to Railway dashboard")
    print("   - Click 'Deploy' button")
    print("   - Wait for deployment to complete")

def show_railway_cli_fix():
    """Show Railway CLI fix commands"""
    print("\n🚀 Railway CLI Fix Commands:")
    print("=" * 30)
    
    print("   # Remove PostgreSQL variables")
    print("   railway variables unset POSTGRES_URL")
    print("   railway variables unset POSTGRES_DB")
    print("   railway variables unset POSTGRES_USER")
    print("   railway variables unset POSTGRES_PASSWORD")
    
    print("\n   # Set MongoDB variables")
    print("   railway variables set MONGODB_URI=\"mongodb+srv://aamp898989:dronesurvillance@cluster0.cftmhkh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0\"")
    print("   railway variables set DATABASE_NAME=\"drone_alerts_db\"")
    print("   railway variables set DATABASE_URL=\"mongodb+srv://aamp898989:dronesurvillance@cluster0.cftmhkh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0\"")
    
    print("\n   # Deploy")
    print("   railway up")

def main():
    """Main function"""
    print("🚁 Disable PostgreSQL - Use MongoDB")
    print("=" * 50)
    
    # Check environment
    check_environment()
    
    # Show Railway fix
    show_railway_fix()
    
    # Show CLI fix
    show_railway_cli_fix()
    
    print("\n💡 Key Points:")
    print("=" * 30)
    print("1. Railway automatically detects database dependencies")
    print("2. If it finds PostgreSQL variables, it tries to use PostgreSQL")
    print("3. We need to explicitly set DATABASE_URL to MongoDB")
    print("4. Remove any PostgreSQL-related variables")
    
    print("\n🎯 Expected Results:")
    print("   ✅ No more psycopg2 errors")
    print("   ✅ MongoDB connection successful")
    print("   ✅ All API endpoints working")

if __name__ == "__main__":
    main() 