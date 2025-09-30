"""
Pydantic schemas for medication verification
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, time

from .pill_schemas import PillInfo

class MedicationSchedule(BaseModel):
    """Medication schedule information"""
    patient_id: str = Field(..., description="Patient identifier")
    medication_name: str = Field(..., description="Name of medication")
    dosage: str = Field(..., description="Dosage amount")
    frequency: str = Field(..., description="How often to take (e.g., 'twice daily')")
    times: List[time] = Field(..., description="Specific times to take medication")
    start_date: datetime = Field(..., description="When to start taking")
    end_date: Optional[datetime] = Field(None, description="When to stop taking")
    instructions: Optional[str] = Field(None, description="Special instructions")
    prescriber: Optional[str] = Field(None, description="Prescribing doctor")

class VerificationRequest(BaseModel):
    """Request to verify medication"""
    patient_id: str = Field(..., description="Patient identifier")
    pill_info: PillInfo = Field(..., description="Identified pill information")
    timestamp: Optional[datetime] = Field(None, description="Time of verification")

class VerificationResponse(BaseModel):
    """Response from medication verification"""
    is_correct: bool = Field(..., description="Whether pill matches schedule")
    scheduled_medication: Optional[MedicationSchedule] = Field(None, description="Expected medication")
    message: str = Field(..., description="Verification message")
    next_dose_time: Optional[datetime] = Field(None, description="When next dose is due")
    warnings: Optional[List[str]] = Field(None, description="Any warnings or alerts")

class IngestionConfirmation(BaseModel):
    """Request to confirm medication ingestion"""
    patient_id: str = Field(..., description="Patient identifier")
    medication_id: str = Field(..., description="Medication identifier")
    image_data: str = Field(..., description="Base64 encoded image of ingestion")
    timestamp: Optional[datetime] = Field(None, description="Time of ingestion")

class IngestionResponse(BaseModel):
    """Response from ingestion confirmation"""
    ingested: bool = Field(..., description="Whether ingestion was detected")
    confidence: float = Field(..., description="Confidence in detection (0.0-1.0)")
    message: str = Field(..., description="Confirmation message")
    dose_logged: Optional[bool] = Field(None, description="Whether dose was logged")