"""
Helper utilities for MedAdhere application
"""
import hashlib
import base64
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import json
import re

def generate_patient_id(name: str, date_of_birth: datetime) -> str:
    """Generate unique patient ID from name and DOB"""
    # Create a unique identifier
    combined = f"{name.lower()}{date_of_birth.strftime('%Y%m%d')}"
    hash_object = hashlib.md5(combined.encode())
    return f"patient_{hash_object.hexdigest()[:8]}"

def validate_image_data(image_data: str) -> bool:
    """Validate base64 encoded image data"""
    try:
        # Check if it's valid base64
        base64.b64decode(image_data)
        return True
    except Exception:
        return False

def calculate_adherence_rate(taken_doses: int, scheduled_doses: int) -> float:
    """Calculate adherence rate percentage"""
    if scheduled_doses == 0:
        return 0.0
    return round((taken_doses / scheduled_doses) * 100, 2)

def parse_medication_times(times_json: str) -> List[str]:
    """Parse medication times from JSON string"""
    try:
        return json.loads(times_json)
    except (json.JSONDecodeError, TypeError):
        return []

def format_medication_times(times: List[str]) -> str:
    """Format medication times as JSON string"""
    return json.dumps(times)

def is_within_time_window(
    current_time: datetime, 
    scheduled_time: datetime, 
    window_minutes: int = 30
) -> bool:
    """Check if current time is within the specified window of scheduled time"""
    time_diff = abs((current_time - scheduled_time).total_seconds() / 60)
    return time_diff <= window_minutes

def get_next_scheduled_time(times: List[str], current_time: datetime) -> Optional[datetime]:
    """Get the next scheduled time from a list of time strings"""
    current_date = current_time.date()
    next_time = None
    
    for time_str in times:
        try:
            # Parse time
            hour, minute = map(int, time_str.split(':'))
            scheduled_datetime = datetime.combine(current_date, datetime.min.time().replace(hour=hour, minute=minute))
            
            # If time has passed today, check tomorrow
            if scheduled_datetime <= current_time:
                scheduled_datetime = datetime.combine(
                    current_date + timedelta(days=1),
                    datetime.min.time().replace(hour=hour, minute=minute)
                )
            
            if next_time is None or scheduled_datetime < next_time:
                next_time = scheduled_datetime
                
        except (ValueError, AttributeError):
            continue
    
    return next_time

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Limit length
    filename = filename[:100]
    return filename

def format_phone_number(phone: str) -> str:
    """Format phone number to standard format"""
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    # Format US phone numbers
    if len(digits) == 10:
        return f"+1-{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"+1-{digits[1:4]}-{digits[4:7]}-{digits[7:]}"
    else:
        return phone  # Return original if can't format

def validate_email(email: str) -> bool:
    """Validate email address format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def get_severity_level(adherence_rate: float) -> str:
    """Get severity level based on adherence rate"""
    if adherence_rate >= 90:
        return "low"
    elif adherence_rate >= 80:
        return "medium"
    elif adherence_rate >= 60:
        return "high"
    else:
        return "critical"

def create_alert_message(
    patient_name: str, 
    medication_name: str, 
    alert_type: str,
    **kwargs
) -> str:
    """Create standardized alert message"""
    messages = {
        "missed_dose": f"{patient_name} missed their {medication_name} dose scheduled for {kwargs.get('scheduled_time', 'now')}.",
        "low_adherence": f"{patient_name}'s medication adherence for {medication_name} is {kwargs.get('adherence_rate', 0)}%. Consider intervention.",
        "multiple_missed": f"{patient_name} has missed {kwargs.get('missed_count', 0)} doses of {medication_name} in the past week.",
        "system_error": f"System error detected for {patient_name}'s medication tracking. Please check manually."
    }
    
    return messages.get(alert_type, f"Alert for {patient_name} regarding {medication_name}.")

def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """Split list into chunks of specified size"""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

def safe_json_loads(json_str: str, default: Any = None) -> Any:
    """Safely load JSON string with default fallback"""
    try:
        return json.loads(json_str) if json_str else default
    except (json.JSONDecodeError, TypeError):
        return default

def safe_json_dumps(obj: Any, default: str = "{}") -> str:
    """Safely dump object to JSON string with default fallback"""
    try:
        return json.dumps(obj)
    except (TypeError, ValueError):
        return default