"""
Configuration settings for MedAdhere application
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    database_url: str = "sqlite:///./medadhere.db"
    
    # API Settings
    api_title: str = "MedAdhere API"
    api_version: str = "1.0.0"
    api_description: str = "AI-Powered Medication Adherence System"
    
    # Machine Learning Models
    pill_model_path: str = "data/models/pill_identifier.h5"
    ingestion_model_path: str = "data/models/ingestion_detector.h5"
    
    # Image Processing
    max_image_size: int = 10 * 1024 * 1024  # 10MB
    allowed_image_types: list = ["image/jpeg", "image/png", "image/jpg"]
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Notifications
    twilio_account_sid: Optional[str] = None
    twilio_auth_token: Optional[str] = None
    twilio_phone_number: Optional[str] = None
    
    # Email
    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/medadhere.log"
    
    # Adherence Thresholds
    adherence_warning_threshold: float = 0.8  # 80%
    adherence_critical_threshold: float = 0.6  # 60%
    missed_dose_alert_delay_minutes: int = 30
    
    # Demo / seeding behavior
    # Set to True only for demo/testing; false by default to avoid creating sample data
    seed_demo_data: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()