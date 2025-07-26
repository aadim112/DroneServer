#!/usr/bin/env python3
"""
Railway Startup Script
Handles Railway-specific configuration and startup
"""

import os
import sys
import logging
from pathlib import Path

# Configure logging for Railway
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_railway_environment():
    """Set up Railway-specific environment variables"""
    
    # Set default values for Railway
    if not os.getenv("PORT"):
        os.environ["PORT"] = "8000"
    
    if not os.getenv("HOST"):
        os.environ["HOST"] = "0.0.0.0"
    
    if not os.getenv("ENVIRONMENT"):
        os.environ["ENVIRONMENT"] = "production"
    
    if not os.getenv("DEBUG"):
        os.environ["DEBUG"] = "false"
    
    # Log environment setup
    logger.info(f"Railway Environment Setup:")
    logger.info(f"  PORT: {os.getenv('PORT')}")
    logger.info(f"  HOST: {os.getenv('HOST')}")
    logger.info(f"  ENVIRONMENT: {os.getenv('ENVIRONMENT')}")
    logger.info(f"  DEBUG: {os.getenv('DEBUG')}")
    logger.info(f"  MONGODB_URI: {'Set' if os.getenv('MONGODB_URI') else 'Not Set'}")
    logger.info(f"  DATABASE_NAME: {os.getenv('DATABASE_NAME', 'Not Set')}")

def main():
    """Main startup function for Railway"""
    try:
        logger.info("🚀 Starting Drone Alert Management System on Railway...")
        
        # Set up Railway environment
        setup_railway_environment()
        
        # Check if MongoDB URI is set
        if not os.getenv("MONGODB_URI"):
            logger.error("❌ MONGODB_URI environment variable is not set!")
            logger.error("Please set MONGODB_URI in Railway environment variables")
            sys.exit(1)
        
        # Import and run the production app
        from main_production import app
        import uvicorn
        
        port = int(os.getenv("PORT", 8000))
        host = os.getenv("HOST", "0.0.0.0")
        
        logger.info(f"📡 Starting server on {host}:{port}")
        logger.info(f"🌐 Health check will be available at: http://{host}:{port}/health")
        
        # Start the server
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="info"
        )
        
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        logger.error("Make sure all dependencies are installed")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Startup error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 