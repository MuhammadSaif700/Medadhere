"""
Medication verification and schedule management
"""
from typing import Dict, List, Optional, Any
from datetime import datetime, time, timedelta
import logging
import json
from pathlib import Path

from src.api.schemas.medication_schemas import MedicationSchedule
from src.api.schemas.pill_schemas import PillInfo

logger = logging.getLogger(__name__)

class MedicationVerifier:
    """
    Handles medication verification against patient schedules
    """
    
    def __init__(self, schedules_path: str = "data/medication_schedules.json"):
        self.schedules_path = schedules_path
        self.patient_schedules = {}
        self.dose_logs = {}
        self.medications_path = "data/medications.json"
        self.medications = {}
        
        self._load_schedules()
        self._load_dose_logs()
        # Load medications store after schedules/logs
        self._load_medications()
    
    def _load_schedules(self):
        """Load patient medication schedules"""
        try:
            schedules_file = Path(self.schedules_path)
            if schedules_file.exists():
                with open(schedules_file, 'r') as f:
                    try:
                        data = json.load(f)
                    except Exception:
                        data = {}
                    self.patient_schedules = data
                logger.info(f"Loaded schedules for {len(self.patient_schedules)} patients")
            else:
                # Create an empty schedules file (no sample/demo data)
                self.patient_schedules = {}
                schedules_file.parent.mkdir(parents=True, exist_ok=True)
                with open(self.schedules_path, 'w') as f:
                    json.dump(self.patient_schedules, f, indent=2)
                logger.info("Created empty schedules file (no sample data)")

        except Exception as e:
            logger.error(f"Error loading schedules: {e}")
            # On error, start empty and persist an empty file
            self.patient_schedules = {}
            schedules_file = Path(self.schedules_path)
            schedules_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.schedules_path, 'w') as f:
                json.dump(self.patient_schedules, f, indent=2)
    
    def _create_sample_schedules(self):
        """Create sample medication schedules for demonstration"""
        # Start with an empty schedules file for a clean user experience
        self.patient_schedules = {}
        schedules_dir = Path(self.schedules_path).parent
        schedules_dir.mkdir(parents=True, exist_ok=True)
        # Save empty schedules file
        with open(self.schedules_path, 'w') as f:
            json.dump(self.patient_schedules, f, indent=2)

    def _load_medications(self):
        """Load medications catalog (user-added medications)"""
        try:
            meds_path = Path(self.medications_path)
            if meds_path.exists():
                with open(meds_path, 'r') as f:
                    self.medications = json.load(f)
                logger.info(f"Loaded {len(self.medications)} medications")
            else:
                # Start with empty medications store
                self.medications = {}
                meds_path.parent.mkdir(parents=True, exist_ok=True)
                with open(meds_path, 'w') as f:
                    json.dump(self.medications, f, indent=2)
        except Exception as e:
            logger.error(f"Error loading medications: {e}")
            self.medications = {}

    def add_medication(self, med_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a medication to the medications store and return its id"""
        try:
            # Generate a simple integer id as string
            next_id = 0
            if self.medications:
                existing_ids = [int(k) for k in self.medications.keys() if k.isdigit()]
                next_id = max(existing_ids) + 1 if existing_ids else 0

            med_id = str(next_id)
            # Store medication record
            self.medications[med_id] = med_data

            # Persist
            meds_path = Path(self.medications_path)
            meds_path.parent.mkdir(parents=True, exist_ok=True)
            with open(meds_path, 'w') as f:
                json.dump(self.medications, f, indent=2)

            return {"id": med_id, **med_data}
        except Exception as e:
            logger.error(f"Error adding medication: {e}")
            raise

    def get_medication_by_id(self, med_id: str) -> Optional[Dict[str, Any]]:
        return self.medications.get(str(med_id))

    def clear_all_data(self):
        """Clear in-memory stores and delete persisted files for a clean slate."""
        try:
            # Clear in-memory
            self.patient_schedules = {}
            self.dose_logs = {}
            self.medications = {}

            # Remove files if exist
            for p in [self.schedules_path, 'data/dose_logs.json', self.medications_path]:
                fp = Path(p)
                try:
                    if fp.exists():
                        fp.unlink()
                except Exception:
                    pass

            # Recreate empty files
            Path(self.schedules_path).parent.mkdir(parents=True, exist_ok=True)
            with open(self.schedules_path, 'w') as f:
                json.dump(self.patient_schedules, f, indent=2)
            with open('data/dose_logs.json', 'w') as f:
                json.dump(self.dose_logs, f, indent=2)
            with open(self.medications_path, 'w') as f:
                json.dump(self.medications, f, indent=2)

            logger.info('Cleared schedules, dose logs, and medications (in-memory and on-disk)')
            return True
        except Exception as e:
            logger.error(f'Error clearing all data: {e}')
            return False
    
    def _load_dose_logs(self):
        """Load dose taking logs"""
        try:
            logs_path = Path("data/dose_logs.json")
            if logs_path.exists():
                with open(logs_path, 'r') as f:
                    self.dose_logs = json.load(f)
            else:
                self.dose_logs = {}
                
        except Exception as e:
            logger.error(f"Error loading dose logs: {e}")
            self.dose_logs = {}
    
    def verify_medication(
        self, 
        patient_id: str, 
        pill_info: PillInfo, 
        timestamp: datetime
    ) -> Dict[str, Any]:
        """
        Verify if the identified pill matches scheduled medication
        
        Args:
            patient_id: Patient identifier
            pill_info: Information about identified pill
            timestamp: Time of verification
            
        Returns:
            Verification result with details
        """
        try:
            if patient_id not in self.patient_schedules:
                return {
                    "is_correct": False,
                    "message": "No medication schedule found for patient",
                    "scheduled_medication": None
                }
            
            current_time = timestamp.time()
            current_date = timestamp.date()
            
            # Find medications scheduled around this time
            scheduled_meds = self._get_scheduled_medications(patient_id, current_time)
            
            if not scheduled_meds:
                return {
                    "is_correct": False,
                    "message": "No medications scheduled at this time",
                    "scheduled_medication": None,
                    "next_dose_time": self._get_next_dose_time(patient_id, timestamp)
                }
            
            # Check if pill matches any scheduled medication
            for scheduled_med in scheduled_meds:
                if self._pills_match(pill_info, scheduled_med):
                    return {
                        "is_correct": True,
                        "message": "Correct medication for scheduled time",
                        "scheduled_medication": scheduled_med,
                        "next_dose_time": self._get_next_dose_time(patient_id, timestamp)
                    }
            
            return {
                "is_correct": False,
                "message": "Pill does not match scheduled medication",
                "scheduled_medication": scheduled_meds[0],  # Show expected medication
                "next_dose_time": self._get_next_dose_time(patient_id, timestamp)
            }
            
        except Exception as e:
            logger.error(f"Error verifying medication: {e}")
            return {
                "is_correct": False,
                "message": "Error during verification",
                "scheduled_medication": None
            }
    
    def _get_scheduled_medications(self, patient_id: str, current_time: time) -> List[Dict[str, Any]]:
        """Get medications scheduled around the current time"""
        scheduled = []
        time_window = 30  # 30 minute window
        
        for med_schedule in self.patient_schedules.get(patient_id, []):
            for scheduled_time_str in med_schedule["times"]:
                scheduled_time = datetime.strptime(scheduled_time_str, "%H:%M").time()
                
                # Check if current time is within window of scheduled time
                current_minutes = current_time.hour * 60 + current_time.minute
                scheduled_minutes = scheduled_time.hour * 60 + scheduled_time.minute
                
                if abs(current_minutes - scheduled_minutes) <= time_window:
                    scheduled.append(med_schedule)
                    break
        
        return scheduled
    
    def _pills_match(self, pill_info: PillInfo, scheduled_med: Dict[str, Any]) -> bool:
        """Check if identified pill matches scheduled medication"""
        # Simple name and dosage matching
        return (
            pill_info.name.lower() == scheduled_med["medication_name"].lower() and
            pill_info.dosage == scheduled_med["dosage"]
        )
    
    def _get_next_dose_time(self, patient_id: str, current_time: datetime) -> Optional[datetime]:
        """Get the next scheduled dose time for patient"""
        next_dose = None
        current_date = current_time.date()
        
        for med_schedule in self.patient_schedules.get(patient_id, []):
            for time_str in med_schedule["times"]:
                dose_time = datetime.strptime(time_str, "%H:%M").time()
                dose_datetime = datetime.combine(current_date, dose_time)
                
                # If time has passed today, check tomorrow
                if dose_datetime <= current_time:
                    dose_datetime = datetime.combine(
                        current_date + timedelta(days=1), 
                        dose_time
                    )
                
                if next_dose is None or dose_datetime < next_dose:
                    next_dose = dose_datetime
        
        return next_dose
    
    def log_dose_taken(
        self, 
        patient_id: str, 
        medication_id: str, 
        timestamp: datetime,
        confidence: float = 1.0
    ):
        """Log that a dose was successfully taken"""
        try:
            if patient_id not in self.dose_logs:
                self.dose_logs[patient_id] = []
            
            dose_entry = {
                "medication_id": medication_id,
                "timestamp": timestamp.isoformat(),
                "confidence": confidence,
                "status": "taken"
            }
            
            self.dose_logs[patient_id].append(dose_entry)
            
            # Save updated logs
            logs_path = Path("data/dose_logs.json")
            logs_path.parent.mkdir(exist_ok=True)
            with open(logs_path, 'w') as f:
                json.dump(self.dose_logs, f, indent=2)
            
            logger.info(f"Logged dose for patient {patient_id}")
            
        except Exception as e:
            logger.error(f"Error logging dose: {e}")
    
    def get_patient_schedule(self, patient_id: str) -> List[MedicationSchedule]:
        """Get medication schedule for a patient"""
        if patient_id not in self.patient_schedules:
            return []
        
        schedules = []
        for med_data in self.patient_schedules[patient_id]:
            # Convert times to time objects
            times = [datetime.strptime(t, "%H:%M").time() for t in med_data["times"]]
            
            schedule = MedicationSchedule(
                patient_id=patient_id,
                medication_name=med_data["medication_name"],
                dosage=med_data["dosage"],
                frequency=med_data["frequency"],
                times=times,
                start_date=datetime.fromisoformat(med_data["start_date"]),
                end_date=datetime.fromisoformat(med_data["end_date"]) if med_data.get("end_date") else None,
                instructions=med_data.get("instructions"),
                prescriber=med_data.get("prescriber")
            )
            schedules.append(schedule)
        
        return schedules
    
    def add_to_schedule(self, schedule: MedicationSchedule) -> Dict[str, Any]:
        """Add medication to patient's schedule"""
        try:
            if schedule.patient_id not in self.patient_schedules:
                self.patient_schedules[schedule.patient_id] = []
            
            med_data = {
                "medication_name": schedule.medication_name,
                "dosage": schedule.dosage,
                "frequency": schedule.frequency,
                "times": [t.strftime("%H:%M") for t in schedule.times],
                "start_date": schedule.start_date.isoformat(),
                "end_date": schedule.end_date.isoformat() if schedule.end_date else None,
                "instructions": schedule.instructions,
                "prescriber": schedule.prescriber
            }
            
            self.patient_schedules[schedule.patient_id].append(med_data)
            
            # Save updated schedules
            schedules_dir = Path(self.schedules_path).parent
            schedules_dir.mkdir(exist_ok=True)
            with open(self.schedules_path, 'w') as f:
                json.dump(self.patient_schedules, f, indent=2)
            
            return {"schedule_id": len(self.patient_schedules[schedule.patient_id]) - 1}
            
        except Exception as e:
            logger.error(f"Error adding to schedule: {e}")
            raise

    def delete_from_schedule(self, patient_id: str, schedule_index: int) -> bool:
        """Delete a scheduled medication by index for a patient

        Returns True if deleted, False if not found
        """
        try:
            if patient_id not in self.patient_schedules:
                return False

            schedules = self.patient_schedules[patient_id]
            if schedule_index < 0 or schedule_index >= len(schedules):
                return False

            # Remove the schedule entry
            schedules.pop(schedule_index)

            # Save updated schedules
            schedules_dir = Path(self.schedules_path).parent
            schedules_dir.mkdir(exist_ok=True)
            with open(self.schedules_path, 'w') as f:
                json.dump(self.patient_schedules, f, indent=2)

            return True
        except Exception as e:
            logger.error(f"Error deleting schedule: {e}")
            return False