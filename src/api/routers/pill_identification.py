"""
Pill identification API endpoints
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from typing import List, Optional
import numpy as np
from PIL import Image
import io
import logging
from datetime import datetime
from pydantic import BaseModel

from ...api.schemas.pill_schemas import PillIdentificationResponse, PillInfo
from ...models.pill_identifier import PillIdentifier
from ...vision.image_processor_simple import ImageProcessor
from ...services.pill_data_service import PillDataService
from ...services.pill_ocr_service import PillOCRService
from ...models.medication_verifier import MedicationVerifier

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize services
pill_identifier = PillIdentifier()
image_processor = ImageProcessor()
pill_data_service = PillDataService()
ocr_service = PillOCRService()
medication_verifier = MedicationVerifier()

# Request model for logging dose
class LogDoseRequest(BaseModel):
    medication_name: str
    dosage: str
    patient_id: str = "default_user"

@router.post("/identify", response_model=PillIdentificationResponse)
async def identify_pill(
    image: UploadFile = File(...),
    confidence_threshold: float = 0.3
):
    """
    Identify a pill from an uploaded image using OCR and external medical databases
    
    Args:
        image: Uploaded image file
        confidence_threshold: Minimum confidence for identification
        
    Returns:
        PillIdentificationResponse with identified pill information
    """
    try:
        # Validate image file
        if not image.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail="File must be an image"
            )
        
        # Read and process image
        image_data = await image.read()
        pil_image = Image.open(io.BytesIO(image_data))
        
        # Step 1: Try OCR to extract imprint text
        imprint_text = ocr_service.extract_text(pil_image)
        logger.info(f"Extracted imprint: '{imprint_text}'")
        
        # Step 2: Search external databases
        search_results = []
        
        # Try searching by any text found in the image
        if imprint_text and len(imprint_text.strip()) >= 2:
            logger.info(f"Attempting to search with extracted text: '{imprint_text}'")
            
            # First try imprint search
            imprint_results = await pill_data_service.search_by_imprint(imprint_text)
            if imprint_results:
                search_results.extend(imprint_results)
                logger.info(f"Found {len(imprint_results)} results from imprint search")
            
            # Also try name search with the extracted text (might be medication name on packaging)
            if not search_results or len(search_results) < 5:
                name_results = await pill_data_service.search_by_name(imprint_text)
                if name_results:
                    logger.info(f"Found {len(name_results)} results from name search")
                    # Add name results that aren't duplicates
                    for result in name_results:
                        if not any(r.get('name', '').lower() == result.get('name', '').lower() for r in search_results):
                            search_results.append(result)
        
        # Step 3: Also do visual identification with local model as fallback
        processed_image = image_processor.preprocess_for_identification(pil_image)
        local_result = pill_identifier.identify(
            processed_image,
            confidence_threshold=confidence_threshold
        )
        
        # Step 4: Combine results
        if search_results:
            # Use external API results (more reliable)
            best_match = search_results[0]
            
            pill_info = PillInfo(
                name=best_match.get("name", "Unknown"),
                dosage=best_match.get("dosage", "Unknown"),
                shape=best_match.get("shape", "unknown"),
                color=best_match.get("color", "unknown"),
                imprint=imprint_text or best_match.get("imprint"),
                manufacturer=best_match.get("manufacturer", "Unknown"),
                ndc_number=best_match.get("ndc_number")
            )
            
            return PillIdentificationResponse(
                success=True,
                pill_info=pill_info,
                confidence=0.9,  # High confidence for API matches
                message=f"Pill identified from medical database{' (detected text: ' + imprint_text + ')' if imprint_text else ''}"
            )
        elif local_result:
            # Fall back to local identification
            return PillIdentificationResponse(
                success=True,
                pill_info=local_result["pill_info"],
                confidence=local_result["confidence"],
                message="Pill identified from local database"
            )
        else:
            # Provide helpful message
            extracted_hint = f" (detected text: '{imprint_text}')" if imprint_text else ""
            return PillIdentificationResponse(
                success=False,
                message=f"Could not identify pill with sufficient confidence{extracted_hint}. Try using the Pill Database search with the medication name.",
                confidence=0.0
            )
        
    except Exception as e:
        logger.error(f"Error identifying pill: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Error processing image for pill identification"
        )


@router.post("/", response_model=dict)
async def create_pill(pill: PillInfo):
    """Create a new pill entry in the pill database"""
    try:
        stored = pill_identifier.add_pill(pill.dict())
        return {"success": True, "pill": stored}
    except Exception as e:
        logger.error(f"Error creating pill: {e}")
        raise HTTPException(status_code=500, detail="Error creating pill entry")

@router.get("/database", response_model=List[PillInfo])
async def get_pill_database():
    """
    Get all pills in the identification database
    
    Returns:
        List of PillInfo objects
    """
    try:
        pills = pill_identifier.get_all_pills()
        return pills
    except Exception as e:
        logger.error(f"Error retrieving pill database: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error retrieving pill database"
        )

@router.get("/search")
async def search_pills(
    name: Optional[str] = None,
    imprint: Optional[str] = None,
    color: Optional[str] = None,
    shape: Optional[str] = None
):
    """
    Search pills by various attributes using local database and external medical APIs
    
    Args:
        name: Medication name
        imprint: Pill imprint text
        color: Pill color
        shape: Pill shape
        
    Returns:
        List of matching pills
    """
    try:
        logger.info(f"Search request - name: {name}, imprint: {imprint}, color: {color}, shape: {shape}")
        all_results = []
        
        # Step 1: Search external APIs
        if name:
            logger.info(f"Searching external APIs for: {name}")
            external_results = await pill_data_service.search_by_name(name)
            logger.info(f"Found {len(external_results)} results from external APIs")
            
            # Convert external results to PillInfo format
            for result in external_results[:10]:  # Limit to top 10
                pill_info = PillInfo(
                    name=result.get("name", "Unknown"),
                    dosage=result.get("dosage", "Unknown"),
                    shape=result.get("shape", "unknown"),
                    color=result.get("color", "unknown"),
                    imprint=result.get("imprint"),
                    manufacturer=result.get("manufacturer", "Unknown"),
                    ndc_number=result.get("ndc_number")
                )
                all_results.append(pill_info)
        
        if imprint and not name:
            external_results = await pill_data_service.search_by_imprint(imprint)
            
            # Convert external results to PillInfo format
            for result in external_results[:10]:
                pill_info = PillInfo(
                    name=result.get("name", "Unknown"),
                    dosage=result.get("dosage", "Unknown"),
                    shape=result.get("shape", "unknown"),
                    color=result.get("color", "unknown"),
                    imprint=result.get("imprint"),
                    manufacturer=result.get("manufacturer", "Unknown"),
                    ndc_number=result.get("ndc_number")
                )
                all_results.append(pill_info)
        
        # Step 2: Also search local database
        search_criteria = {}
        if name:
            search_criteria["name"] = name
        if imprint:
            search_criteria["imprint"] = imprint
        if color:
            search_criteria["color"] = color
        if shape:
            search_criteria["shape"] = shape
            
        if search_criteria:
            local_results = pill_identifier.search_pills(search_criteria)
            
            # Add local results if not duplicates
            for local_pill in local_results:
                # Check if already in results (by name+dosage)
                is_duplicate = any(
                    r.name.lower() == local_pill.name.lower() and 
                    r.dosage == local_pill.dosage 
                    for r in all_results
                )
                if not is_duplicate:
                    all_results.append(local_pill)
        
        return all_results
        
    except Exception as e:
        logger.error(f"Error searching pills: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Error searching pill database"
        )


@router.post("/log-dose", response_model=dict)
async def log_identified_dose(request: LogDoseRequest):
    """
    Log a dose after pill identification
    
    Args:
        request: LogDoseRequest with medication name, dosage, and patient ID
        
    Returns:
        Success message with logged dose information
    """
    try:
        # Check if medication exists, if not create it
        medication_id = f"{request.medication_name}_{request.dosage}".replace(" ", "_").lower()
        
        # Try to get existing medication
        existing_med = medication_verifier.get_medication_by_id(medication_id)
        
        if not existing_med:
            # Add new medication
            medication_data = {
                "medication_id": medication_id,
                "name": request.medication_name,
                "dosage": request.dosage,
                "type": "tablet"
            }
            medication_verifier.add_medication(medication_data)
            logger.info(f"Added new medication: {medication_id}")
        
        # Log the dose
        medication_verifier.log_dose_taken(
            patient_id=request.patient_id,
            medication_id=medication_id,
            timestamp=datetime.now(),
            confidence=0.9
        )
        
        logger.info(f"Logged dose for {request.medication_name} ({request.dosage}) for patient {request.patient_id}")
        
        return {
            "success": True,
            "message": f"Dose logged successfully for {request.medication_name} ({request.dosage})",
            "medication_id": medication_id,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error logging dose: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Error logging dose"
        )