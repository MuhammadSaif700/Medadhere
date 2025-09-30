"""
Adherence tracking API endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from datetime import datetime, timedelta
from typing import List, Optional

from ...api.schemas.adherence_schemas import (
    AdherenceReport,
    AdherenceStats,
    MissedDose,
    CaregiverAlert
)
from ...models.adherence_tracker import AdherenceTracker

router = APIRouter()

# Initialize service
adherence_tracker = AdherenceTracker()

@router.get("/report/{patient_id}", response_model=AdherenceReport)
async def get_adherence_report(
    patient_id: str,
    days: int = Query(default=30, description="Number of days to include in report")
):
    """
    Get adherence report for a patient
    
    Args:
        patient_id: Patient identifier
        days: Number of days to include in report
        
    Returns:
        Comprehensive adherence report
    """
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        report = adherence_tracker.generate_report(
            patient_id=patient_id,
            start_date=start_date,
            end_date=end_date
        )
        
        return report
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating adherence report: {str(e)}"
        )

@router.get("/stats/{patient_id}", response_model=AdherenceStats)
async def get_adherence_stats(patient_id: str):
    """
    Get current adherence statistics for a patient
    
    Args:
        patient_id: Patient identifier
        
    Returns:
        Current adherence statistics
    """
    try:
        stats = adherence_tracker.get_current_stats(patient_id)
        return stats
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving adherence stats: {str(e)}"
        )

@router.get("/missed-doses/{patient_id}", response_model=List[MissedDose])
async def get_missed_doses(
    patient_id: str,
    days: int = Query(default=7, description="Number of days to check")
):
    """
    Get missed doses for a patient
    
    Args:
        patient_id: Patient identifier
        days: Number of days to check
        
    Returns:
        List of missed doses
    """
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        missed_doses = adherence_tracker.get_missed_doses(
            patient_id=patient_id,
            start_date=start_date,
            end_date=end_date
        )
        
        return missed_doses
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving missed doses: {str(e)}"
        )

@router.post("/alert", response_model=dict)
async def send_caregiver_alert(alert: CaregiverAlert):
    """
    Send alert to caregiver about missed medication
    
    Args:
        alert: Caregiver alert information
        
    Returns:
        Success confirmation
    """
    try:
        result = adherence_tracker.send_caregiver_alert(alert)
        return {"success": True, "alert_id": result["alert_id"]}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error sending caregiver alert: {str(e)}"
        )

@router.get("/trends/{patient_id}")
async def get_adherence_trends(
    patient_id: str,
    days: int = Query(default=90, description="Number of days for trend analysis")
):
    """
    Get adherence trends and patterns for a patient
    
    Args:
        patient_id: Patient identifier
        days: Number of days for analysis
        
    Returns:
        Adherence trends and insights
    """
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        trends = adherence_tracker.analyze_trends(
            patient_id=patient_id,
            start_date=start_date,
            end_date=end_date
        )
        
        return trends
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing adherence trends: {str(e)}"
        )