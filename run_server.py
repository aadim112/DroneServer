#!/usr/bin/env python3
"""
Server Runner Script
Simple script to run the drone alert management server
"""

import sys
import os
import asyncio
import logging
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from main import app
    from config import Config
    import uvicorn
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please make sure all dependencies are installed:")
    print("pip install -r requirements.txt")
    sys.exit(1)

def main():
    """Main function to run the server"""
    print("🚁 Starting Drone Alert Management System...")
    print(f"📡 Server will be available at: http://{Config.HOST}:{Config.PORT}")
    print(f"📚 API Documentation: http://{Config.HOST}:{Config.PORT}/docs")
    print(f"📊 Dashboard: http://{Config.HOST}:{Config.PORT}/dashboard/")
    print("=" * 50)
    
    try:
        uvicorn.run(
            "main:app",
            host=Config.HOST,
            port=Config.PORT,
            reload=True,
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 