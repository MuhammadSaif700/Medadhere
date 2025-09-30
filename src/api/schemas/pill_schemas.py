"""
Pydantic schemas for pill identification
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class PillInfo(BaseModel):
    """Information about an identified pill"""
    name: str = Field(..., description="Medication name")
    dosage: str = Field(..., description="Dosage amount")
    shape: str = Field(..., description="Pill shape")
    color: str = Field(..., description="Pill color")
    imprint: Optional[str] = Field(None, description="Text/numbers on pill")
    size: Optional[str] = Field(None, description="Pill size")
    ndc_number: Optional[str] = Field(None, description="National Drug Code")
    manufacturer: Optional[str] = Field(None, description="Manufacturer name")
    
class PillIdentificationResponse(BaseModel):
    """Response from pill identification"""
    success: bool = Field(..., description="Whether identification was successful")
    pill_info: Optional[PillInfo] = Field(None, description="Identified pill information")
    confidence: float = Field(..., description="Confidence score (0.0-1.0)")
    message: str = Field(..., description="Human-readable message")
    alternatives: Optional[List[PillInfo]] = Field(None, description="Alternative matches")
    
class PillSearchRequest(BaseModel):
    """Request for searching pills in database"""
    name: Optional[str] = None
    imprint: Optional[str] = None
    color: Optional[str] = None
    shape: Optional[str] = None
    manufacturer: Optional[str] = None
    
class PillSearchResponse(BaseModel):
    """Response from pill search"""
    results: List[PillInfo]
    total_count: int
    search_criteria: Dict[str, Any]