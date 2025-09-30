"""
Pydantic schemas for adherence tracking
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class MissedDose(BaseModel):
    """Information about a missed dose"""
    patient_id: str = Field(..., description="Patient identifier")
    medication_name: str = Field(..., description="Name of missed medication")
    scheduled_time: datetime = Field(..., description="When dose was scheduled")
    missed_time: datetime = Field(..., description="When system detected miss")
    severity: str = Field(..., description="Severity of missing dose")
    
class AdherenceStats(BaseModel):
    """Current adherence statistics"""
    patient_id: str = Field(..., description="Patient identifier")
    overall_adherence_rate: float = Field(..., description="Overall adherence percentage")
    doses_taken_today: int = Field(..., description="Doses taken today")
    doses_scheduled_today: int = Field(..., description="Doses scheduled today")
    current_streak: int = Field(..., description="Current adherence streak in days")
    longest_streak: int = Field(..., description="Longest adherence streak")
    last_dose_time: Optional[datetime] = Field(None, description="Time of last taken dose")
    
class AdherenceReport(BaseModel):
    """Comprehensive adherence report"""
    patient_id: str = Field(..., description="Patient identifier")
    report_period: Dict[str, datetime] = Field(..., description="Start and end dates")
    overall_stats: AdherenceStats = Field(..., description="Overall statistics")
    daily_adherence: List[Dict[str, Any]] = Field(..., description="Daily adherence data")
    missed_doses: List[MissedDose] = Field(..., description="List of missed doses")
    medication_breakdown: Dict[str, float] = Field(..., description="Adherence by medication")
    recommendations: List[str] = Field(..., description="Improvement recommendations")
    
class CaregiverAlert(BaseModel):
    """Alert to send to caregiver"""
    patient_id: str = Field(..., description="Patient identifier")
    caregiver_contact: str = Field(..., description="Caregiver phone/email")
    alert_type: str = Field(..., description="Type of alert")
    message: str = Field(..., description="Alert message")
    severity: str = Field(..., description="Alert severity level")
    timestamp: Optional[datetime] = Field(None, description="Alert timestamp")
    
class TrendAnalysis(BaseModel):
    """Adherence trend analysis"""
    patient_id: str = Field(..., description="Patient identifier")
    trend_direction: str = Field(..., description="Overall trend (improving/declining/stable)")
    weekly_averages: List[float] = Field(..., description="Weekly adherence averages")
    patterns: Dict[str, Any] = Field(..., description="Identified patterns")
    risk_factors: List[str] = Field(..., description="Identified risk factors")
    insights: List[str] = Field(..., description="Key insights")