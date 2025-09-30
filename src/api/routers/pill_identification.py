"""
Pill identification API endpoints
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from typing import List, Optional
import numpy as np
from PIL import Image
import io
import logging

from ...api.schemas.pill_schemas import PillIdentificationResponse, PillInfo
from ...models.pill_identifier import PillIdentifier
from ...vision.image_processor_simple import ImageProcessor

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize services
pill_identifier = PillIdentifier()
image_processor = ImageProcessor()

@router.post("/identify", response_model=PillIdentificationResponse)
async def identify_pill(
    image: UploadFile = File(...),
    confidence_threshold: float = 0.8
):
    """
    Identify a pill from an uploaded image
    
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
        
        # Preprocess image for model
        processed_image = image_processor.preprocess_for_identification(pil_image)
        
        # Identify pill using ML model
        identification_result = pill_identifier.identify(
            processed_image,
            confidence_threshold=confidence_threshold
        )
        
        if not identification_result:
            return PillIdentificationResponse(
                success=False,
                message="No pill identified with sufficient confidence",
                confidence=0.0
            )
        
        return PillIdentificationResponse(
            success=True,
            pill_info=identification_result["pill_info"],
            confidence=identification_result["confidence"],
            message="Pill identified successfully"
        )
        
    except Exception as e:
        logger.error(f"Error identifying pill: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error processing image for pill identification"
        )

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
    Search pills by various attributes
    
    Args:
        name: Medication name
        imprint: Pill imprint text
        color: Pill color
        shape: Pill shape
        
    Returns:
        List of matching pills
    """
    try:
        search_criteria = {}
        if name:
            search_criteria["name"] = name
        if imprint:
            search_criteria["imprint"] = imprint
        if color:
            search_criteria["color"] = color
        if shape:
            search_criteria["shape"] = shape
            
        results = pill_identifier.search_pills(search_criteria)
        return results
        
    except Exception as e:
        logger.error(f"Error searching pills: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error searching pill database"
        )