#!/usr/bin/env python3
"""
Force Railway Redeployment
"""

import subprocess
import os
import json
from datetime import datetime

def check_git_status():
    """Check git status and commit changes"""
    print("🔍 Checking Git Status...")
    
    try:
        # Check if we're in a git repository
        result = subprocess.run(["git", "status"], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Not a git repository")
            return False
        
        print("✅ Git repository found")
        
        # Check for changes
        result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if result.stdout.strip():
            print("📋 Changes detected:")
            print(result.stdout)
            
            # Add all changes
            print("\n📋 Adding changes...")
            subprocess.run(["git", "add", "."], check=True)
            
            # Commit changes
            commit_message = f"Force redeploy - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            print(f"📋 Committing: {commit_message}")
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            
            # Push to trigger Railway deployment
            print("📋 Pushing to trigger Railway deployment...")
            subprocess.run(["git", "push"], check=True)
            
            print("✅ Changes pushed successfully!")
            return True
        else:
            print("📋 No changes detected")
            
            # Force a commit to trigger deployment
            print("📋 Creating empty commit to force deployment...")
            subprocess.run(["git", "commit", "--allow-empty", "-m", f"Force redeploy - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"], check=True)
            subprocess.run(["git", "push"], check=True)
            
            print("✅ Empty commit pushed successfully!")
            return True
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Git error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_railway_files():
    """Check Railway configuration files"""
    print("\n📋 Checking Railway Files...")
    
    files_to_check = [
        ("main.py", "Main application"),
        ("Procfile", "Railway Procfile"),
        ("railway.json", "Railway configuration"),
        ("requirements.txt", "Dependencies")
    ]
    
    for file_path, description in files_to_check:
        if os.path.exists(file_path):
            print(f"   ✅ {description}: {file_path}")
            
            # Show file contents for key files
            if file_path in ["Procfile", "railway.json"]:
                try:
                    with open(file_path, 'r') as f:
                        content = f.read().strip()
                        print(f"      Content: {content}")
                except Exception as e:
                    print(f"      Error reading: {e}")
        else:
            print(f"   ❌ {description}: {file_path} - MISSING")

def show_railway_dashboard_steps():
    """Show steps to check Railway dashboard"""
    print("\n🌐 Railway Dashboard Steps:")
    print("=" * 50)
    
    print("\n📋 Step 1: Check Deployment Status")
    print("   1. Go to https://railway.app/dashboard")
    print("   2. Select your project")
    print("   3. Check if deployment is in progress")
    print("   4. Wait for deployment to complete")
    
    print("\n📋 Step 2: Check Environment Variables")
    print("   1. Go to Variables tab")
    print("   2. Verify MONGODB_URI is set")
    print("   3. Add if missing: MONGODB_URI=your_mongodb_connection_string")
    
    print("\n📋 Step 3: Check Logs")
    print("   1. Go to Deployments tab")
    print("   2. Click on latest deployment")
    print("   3. Check build logs for errors")
    print("   4. Check runtime logs for startup issues")
    
    print("\n📋 Step 4: Verify Deployment")
    print("   1. Wait 2-3 minutes after push")
    print("   2. Test server: python test_railway.py")
    print("   3. Check if endpoints are working")

def show_manual_deploy_steps():
    """Show manual deployment steps"""
    print("\n🚀 Manual Deployment Steps:")
    print("=" * 50)
    
    print("\n📋 Option 1: Railway CLI")
    print("   1. Install: npm install -g @railway/cli")
    print("   2. Login: railway login")
    print("   3. Link: railway link")
    print("   4. Deploy: railway up")
    
    print("\n📋 Option 2: GitHub Integration")
    print("   1. Push to GitHub (already done)")
    print("   2. Railway auto-deploys from GitHub")
    print("   3. Check deployment status in dashboard")
    
    print("\n📋 Option 3: Force Redeploy")
    print("   1. Go to Railway dashboard")
    print("   2. Select your project")
    print("   3. Click 'Deploy' button")
    print("   4. Wait for deployment to complete")

def main():
    """Main function"""
    print("🚁 Force Railway Redeployment")
    print("=" * 50)
    
    # Check Railway files
    check_railway_files()
    
    # Check git status and push
    git_success = check_git_status()
    
    # Show dashboard steps
    show_railway_dashboard_steps()
    
    # Show manual deploy steps
    show_manual_deploy_steps()
    
    print("\n💡 Summary:")
    print("=" * 50)
    print(f"   Git Push: {'✅ Successful' if git_success else '❌ Failed'}")
    print("   Next: Check Railway dashboard")
    print("   Wait: 2-3 minutes for deployment")
    print("   Test: python test_railway.py")
    
    print("\n🎯 Expected Results After Redeploy:")
    print("   ✅ / - Root endpoint working")
    print("   ✅ /health - Health check working")
    print("   ✅ /api/alerts - Alerts endpoint working")
    print("   ✅ /api/stats - Stats endpoint working")
    print("   ✅ Database connection working")

if __name__ == "__main__":
    main() 