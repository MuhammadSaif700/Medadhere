"""
Medication verification API endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, time
from typing import List, Optional

from ...api.schemas.medication_schemas import (
    MedicationSchedule,
    VerificationRequest,
    VerificationResponse,
    IngestionConfirmation,
    IngestionResponse
)
from ...models.medication_verifier import MedicationVerifier
from ...models.ingestion_detector import IngestionDetector

router = APIRouter()

# Initialize services
medication_verifier = MedicationVerifier()
ingestion_detector = IngestionDetector()


@router.post("/", status_code=200)
async def create_medication(med: dict):
    """Create or register a medication in the medications store

    The frontend uses this to create a medication record before adding a schedule.
    """
    try:
        created = medication_verifier.add_medication(med)
        return created
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating medication: {e}")

@router.post("/verify", response_model=VerificationResponse)
async def verify_medication(request: VerificationRequest):
    """
    Verify if the identified pill matches the scheduled medication
    
    Args:
        request: Verification request with pill info and patient ID
        
    Returns:
        VerificationResponse indicating if medication is correct
    """
    try:
        verification_result = medication_verifier.verify_medication(
            patient_id=request.patient_id,
            pill_info=request.pill_info,
            timestamp=request.timestamp or datetime.now()
        )
        
        return VerificationResponse(
            is_correct=verification_result["is_correct"],
            scheduled_medication=verification_result["scheduled_medication"],
            message=verification_result["message"],
            next_dose_time=verification_result.get("next_dose_time")
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error verifying medication: {str(e)}"
        )

@router.post("/confirm-ingestion", response_model=IngestionResponse)
async def confirm_ingestion(confirmation: IngestionConfirmation):
    """
    Confirm that medication has been ingested using action recognition
    
    Args:
        confirmation: Ingestion confirmation with video/image data
        
    Returns:
        IngestionResponse indicating if ingestion was detected
    """
    try:
        ingestion_result = ingestion_detector.detect_ingestion(
            image_data=confirmation.image_data,
            patient_id=confirmation.patient_id,
            medication_id=confirmation.medication_id
        )
        
        if ingestion_result["ingested"]:
            # Log successful dose
            medication_verifier.log_dose_taken(
                patient_id=confirmation.patient_id,
                medication_id=confirmation.medication_id,
                timestamp=datetime.now(),
                confidence=ingestion_result["confidence"]
            )
        
        return IngestionResponse(
            ingested=ingestion_result["ingested"],
            confidence=ingestion_result["confidence"],
            message=ingestion_result["message"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error confirming ingestion: {str(e)}"
        )

@router.get("/schedule/{patient_id}")
async def get_medication_schedule(patient_id: str):
    """
    Get medication schedule for a patient
    
    Args:
        patient_id: Patient identifier
        
    Returns:
        List of scheduled medications
    """
    try:
        schedules = medication_verifier.get_patient_schedule(patient_id)

        # Convert schedules (Pydantic models) into plain dicts and add an id (index)
        schedule_list = []
        for idx, s in enumerate(schedules):
            # s is a MedicationSchedule model - convert to dict
            sd = s.dict()
            # times are time objects; convert to HH:MM strings for the frontend
            sd['times'] = [t.strftime('%H:%M') for t in sd.get('times', [])]
            sd['id'] = idx
            schedule_list.append(sd)

        return schedule_list
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving schedule: {str(e)}"
        )


@router.delete("/schedule/{patient_id}/{schedule_id}")
async def delete_medication_schedule(patient_id: str, schedule_id: int):
    """
    Delete a scheduled medication by patient and schedule index
    """
    try:
        result = medication_verifier.delete_from_schedule(patient_id, schedule_id)
        if result:
            return {"success": True}
        else:
            raise HTTPException(status_code=404, detail="Schedule not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting schedule: {e}")

@router.post("/schedule", response_model=dict)
async def add_medication_to_schedule(payload: dict):
    """
    Add a medication to patient's schedule.

    Accepts payloads from the frontend which may include a medication_id (created earlier).
    If medication_id is present, resolve the medication info and build a MedicationSchedule
    object before adding.
    """
    try:
        # If frontend provided a medication_id, resolve the medication and construct schedule
        if 'medication_id' in payload:
            med_id = payload.get('medication_id')
            med = medication_verifier.get_medication_by_id(med_id)
            if not med:
                raise HTTPException(status_code=404, detail='Medication not found')

            # Build a payload that conforms to MedicationSchedule
            times = payload.get('times', [])
            # Ensure times are in HH:MM strings
            times_list = []
            for t in times:
                if isinstance(t, str):
                    times_list.append(t)

            # Use provided start_date or default to today
            from datetime import datetime
            start_date = payload.get('start_date') or datetime.utcnow().isoformat()

            med_schedule = MedicationSchedule(
                patient_id=payload.get('patient_id'),
                medication_name=med.get('name') or med.get('generic_name') or 'Unknown',
                dosage=med.get('dosage') or med.get('strength') or 'Unknown',
                frequency=payload.get('frequency', 'once daily'),
                times=[__import__('datetime').datetime.strptime(t, '%H:%M').time() for t in times_list],
                start_date=datetime.fromisoformat(start_date),
                end_date=None,
                instructions=payload.get('instructions'),
                prescriber=payload.get('prescriber')
            )

            result = medication_verifier.add_to_schedule(med_schedule)
            return {"success": True, "schedule_id": result["schedule_id"]}

        # Otherwise, try to validate as full MedicationSchedule (fallback)
        else:
            med_schedule = MedicationSchedule(**payload)
            result = medication_verifier.add_to_schedule(med_schedule)
            return {"success": True, "schedule_id": result["schedule_id"]}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding to schedule: {e}")