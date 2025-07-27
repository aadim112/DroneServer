#!/usr/bin/env python3
"""
Deploy Fixes - Helper script to deploy fixes to Railway
"""

import subprocess
import sys
import os

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
        else:
            print(f"   ❌ Failed!")
            print(f"   Error: {result.stderr.strip()}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    return True

def check_git_status():
    """Check git status"""
    print("🔍 Checking Git Status...")
    
    # Check if we're in a git repository
    if not os.path.exists(".git"):
        print("   ❌ Not a git repository!")
        return False
    
    # Check current status
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        changes = result.stdout.strip()
        if changes:
            print(f"   📝 Changes detected:")
            for line in changes.split('\n'):
                if line.strip():
                    print(f"      {line}")
            return True
        else:
            print("   ✅ No changes to commit")
            return False
    else:
        print(f"   ❌ Error checking git status: {result.stderr}")
        return False

def main():
    """Main deployment function"""
    print("🚁 Deploying Fixes to Railway")
    print("=" * 50)
    
    # Check if we have changes to commit
    has_changes = check_git_status()
    
    if has_changes:
        print("\n📋 Summary of fixes to deploy:")
        print("   1. ✅ Fixed Procfile (points to main.py)")
        print("   2. ✅ Updated requirements.txt (added pymongo, python-dotenv)")
        print("   3. ✅ Removed testing files")
        print("   4. ✅ Created deployment guide")
        
        # Ask for confirmation
        response = input("\n🤔 Do you want to deploy these fixes? (y/N): ")
        if response.lower() != 'y':
            print("❌ Deployment cancelled")
            return
        
        # Add all changes
        if not run_command("git add .", "Adding all changes"):
            return
        
        # Commit changes
        if not run_command('git commit -m "Fix deployment issues: update Procfile and requirements.txt"', "Committing changes"):
            return
        
        # Push to remote
        if not run_command("git push origin main", "Pushing to Railway"):
            return
        
        print("\n✅ Deployment initiated!")
        print("\n📋 Next Steps:")
        print("   1. Check Railway dashboard for deployment status")
        print("   2. Wait for build to complete")
        print("   3. Test the server with: python test_deployed_api.py")
        print("   4. Check logs if there are any issues")
        
    else:
        print("\n✅ No changes to deploy!")
        print("   Your server should already be up to date.")
        print("\n🧪 To test the current deployment:")
        print("   python test_deployed_api.py")

if __name__ == "__main__":
    main() 