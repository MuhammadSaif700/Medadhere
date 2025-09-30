"""
FastAPI main application setup
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from .routers import pill_identification, medication_verification, adherence
from .routers import admin as admin_router
from src.database.database import engine
from src.database.models import Base

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables - commented out for initial testing
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MedAdhere API",
    description="AI-Powered Medication Adherence System API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    pill_identification.router,
    prefix="/api/v1/pills",
    tags=["Pill Identification"]
)
app.include_router(
    medication_verification.router,
    prefix="/api/v1/medications",
    tags=["Medication Verification"]
)
app.include_router(
    adherence.router,
    prefix="/api/v1/adherence",
    tags=["Adherence Tracking"]
)

# Admin routes (development only)
app.include_router(
    admin_router.router,
    prefix="/api/v1/admin",
    tags=["Admin"]
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to MedAdhere API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "MedAdhere API"}

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"}
    )