"""
MedAdhere - AI-Powered Medication Adherence System
Main application entry point
"""
import uvicorn
from src.api.main import app
from src.database.init_db import init_database

def main():
    """Initialize and start the MedAdhere application"""
    print("Initializing MedAdhere...")
    
    # Initialize database
    init_database()
    
    print("Starting MedAdhere API server...")
    print("API Documentation: http://localhost:8010/docs")
    print("Health Check: http://localhost:8010/health")
    
    # Start the FastAPI server
    uvicorn.run(
        "src.api.main:app",
        host="127.0.0.1",
        port=8010,
        reload=False,
        log_level="info"
    )

if __name__ == "__main__":
    main()