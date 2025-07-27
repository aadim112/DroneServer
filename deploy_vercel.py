#!/usr/bin/env python3
"""
Vercel Deployment Script
"""

import subprocess
import os
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    print(f"   Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"   ✅ Success!")
            if result.stdout:
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"   ❌ Failed!")
            print(f"   Error: {result.stderr.strip()}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def check_vercel_cli():
    """Check if Vercel CLI is installed"""
    print("🔍 Checking Vercel CLI...")
    
    try:
        result = subprocess.run("vercel --version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ Vercel CLI found: {result.stdout.strip()}")
            return True
        else:
            print("   ❌ Vercel CLI not found")
            return False
    except:
        print("   ❌ Vercel CLI not found")
        return False

def check_files():
    """Check if required files exist"""
    print("🔍 Checking required files...")
    
    required_files = [
        "main_vercel.py",
        "vercel.json",
        "requirements.txt",
        "database.py",
        "models.py",
        "config.py"
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} (missing)")
            missing_files.append(file)
    
    return len(missing_files) == 0

def main():
    """Main deployment function"""
    print("🚀 Vercel Deployment Script")
    print("=" * 50)
    
    # Check prerequisites
    if not check_vercel_cli():
        print("\n❌ Vercel CLI not found!")
        print("   Install it with: npm install -g vercel")
        return
    
    if not check_files():
        print("\n❌ Missing required files!")
        print("   Make sure all files are present before deploying")
        return
    
    print("\n✅ Prerequisites check passed!")
    
    # Check if user is logged in
    print("\n🔍 Checking Vercel login status...")
    if not run_command("vercel whoami", "Checking login status"):
        print("\n❌ Not logged in to Vercel!")
        print("   Run: vercel login")
        return
    
    # Deploy to Vercel
    print("\n🚀 Deploying to Vercel...")
    
    # Ask for deployment type
    response = input("\n🤔 Deploy to production? (y/N): ")
    if response.lower() == 'y':
        if not run_command("vercel --prod", "Deploying to production"):
            return
    else:
        if not run_command("vercel", "Deploying to preview"):
            return
    
    print("\n✅ Deployment completed!")
    print("\n📋 Next Steps:")
    print("   1. Check your Vercel dashboard")
    print("   2. Set environment variables in Vercel dashboard:")
    print("      - MONGODB_URI")
    print("      - DATABASE_NAME")
    print("   3. Test your API endpoints")
    print("   4. Check API documentation at /docs")

if __name__ == "__main__":
    main() 