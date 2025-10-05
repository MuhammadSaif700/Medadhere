"""
OCR service for extracting text from pill images
"""
import logging
from PIL import Image
import numpy as np
import cv2
from typing import Optional, List, Tuple
import os

logger = logging.getLogger(__name__)

# Import and configure pytesseract
try:
    import pytesseract
    # Configure Tesseract path for Windows
    if os.name == 'nt':  # Windows
        tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        if os.path.exists(tesseract_path):
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
except ImportError:
    pytesseract = None
    logger.warning("pytesseract not available")

class PillOCRService:
    """
    Extract text (imprint) from pill images using OCR
    """
    
    def __init__(self):
        self.tesseract_available = self._check_tesseract()
        
    def _check_tesseract(self) -> bool:
        """Check if Tesseract OCR is available"""
        if pytesseract is None:
            return False
        try:
            # Try to get version to verify it's installed
            pytesseract.get_tesseract_version()
            return True
        except Exception as e:
            logger.warning(f"Tesseract not available: {e}. OCR functionality will be limited.")
            return False
    
    def extract_text(self, image: Image.Image) -> str:
        """
        Extract text from pill image or packaging
        
        Args:
            image: PIL Image object
            
        Returns:
            Extracted text string (empty if no text found)
        """
        if not self.tesseract_available:
            logger.warning("OCR requested but Tesseract not available")
            return ""
        
        try:
            import pytesseract
            
            # Preprocess image for better OCR
            preprocessed = self._preprocess_for_ocr(image)
            
            # Try multiple OCR modes for better results
            all_text = []
            
            # Mode 1: General text extraction (for packaging with brand names)
            try:
                config1 = r'--oem 3 --psm 6'  # Assume uniform text block
                text1 = pytesseract.image_to_string(preprocessed, config=config1)
                if text1.strip():
                    all_text.append(text1)
            except Exception:
                pass
            
            # Mode 2: Single line (for pill imprints)
            try:
                config2 = r'--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-'
                text2 = pytesseract.image_to_string(preprocessed, config=config2)
                if text2.strip():
                    all_text.append(text2)
            except Exception:
                pass
            
            # Mode 3: Sparse text (for individual pills)
            try:
                config3 = r'--oem 3 --psm 11'
                text3 = pytesseract.image_to_string(preprocessed, config=config3)
                if text3.strip():
                    all_text.append(text3)
            except Exception:
                pass
            
            # Combine and extract the most meaningful text
            combined_text = ' '.join(all_text)
            
            # Extract medication names (look for common patterns)
            cleaned_text = self._extract_medication_name(combined_text)
            
            logger.info(f"OCR extracted: '{cleaned_text}' from raw text")
            return cleaned_text
            
        except Exception as e:
            logger.error(f"OCR extraction error: {e}")
            return ""
    
    def _preprocess_for_ocr(self, image: Image.Image) -> Image.Image:
        """
        Preprocess image to improve OCR accuracy
        
        Args:
            image: Input PIL Image
            
        Returns:
            Preprocessed PIL Image
        """
        try:
            # Convert PIL to numpy array
            img_array = np.array(image)
            
            # Convert to grayscale if needed
            if len(img_array.shape) == 3:
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = img_array
            
            # Increase contrast
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            enhanced = clahe.apply(gray)
            
            # Denoise
            denoised = cv2.fastNlMeansDenoising(enhanced)
            
            # Apply adaptive thresholding for better text extraction
            binary = cv2.adaptiveThreshold(
                denoised, 255, 
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 11, 2
            )
            
            # Resize to improve OCR (larger is sometimes better)
            height, width = binary.shape
            if height < 100 or width < 100:
                scale = max(200 / height, 200 / width)
                new_width = int(width * scale)
                new_height = int(height * scale)
                binary = cv2.resize(binary, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
            
            # Convert back to PIL
            return Image.fromarray(binary)
            
        except Exception as e:
            logger.error(f"Image preprocessing error: {e}")
            return image
    
    def _clean_text(self, text: str) -> str:
        """
        Clean extracted text
        
        Args:
            text: Raw OCR output
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove extra whitespace and newlines
        text = " ".join(text.split())
        
        # Remove common OCR errors
        text = text.replace("|", "I")
        text = text.replace("0", "O") if text.isalpha() else text
        
        # Keep only alphanumeric and hyphens
        import re
        text = re.sub(r'[^A-Z0-9\-\s]', '', text.upper())
        
        # Remove extra spaces
        text = " ".join(text.split())
        
        return text.strip()
    
    def _extract_medication_name(self, text: str) -> str:
        """
        Extract likely medication name from OCR text
        
        Args:
            text: Raw OCR text
            
        Returns:
            Most likely medication name
        """
        import re
        
        if not text:
            return ""
        
        # Clean the text first
        text = self._clean_text(text)
        
        # Common medication name patterns (capitalize first letter of each word)
        words = text.split()
        
        # Filter out very short words and common packaging text
        stop_words = {'THE', 'AND', 'OR', 'FOR', 'WITH', 'TABLETS', 'CAPSULES', 'MG', 'ML', 
                      'EACH', 'CONTAINS', 'USE', 'ONLY', 'AS', 'DIRECTED', 'WARNING', 'KEEP'}
        
        # Look for capitalized words that might be medication names (longer than 3 chars)
        potential_names = []
        for word in words:
            if len(word) >= 4 and word.upper() not in stop_words:
                # Check if word looks like a medication name (mostly letters)
                if sum(c.isalpha() for c in word) / len(word) > 0.6:
                    potential_names.append(word)
        
        # Return the first valid-looking medication name
        if potential_names:
            # Prefer longer words (likely to be brand names)
            potential_names.sort(key=len, reverse=True)
            return potential_names[0]
        
        # If no good name found, return first meaningful word
        for word in words:
            if len(word) >= 3:
                return word
        
        return text
    
    def extract_pill_region(self, image: Image.Image) -> Optional[Image.Image]:
        """
        Detect and crop the pill region from image
        
        Args:
            image: Input PIL Image
            
        Returns:
            Cropped PIL Image containing the pill, or None if detection fails
        """
        try:
            # Convert to numpy array
            img_array = np.array(image)
            
            # Convert to grayscale
            if len(img_array.shape) == 3:
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = img_array
            
            # Apply Gaussian blur
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Threshold
            _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Find contours
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if not contours:
                return None
            
            # Find largest contour (assumed to be the pill)
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Get bounding box
            x, y, w, h = cv2.boundingRect(largest_contour)
            
            # Add small padding
            padding = 10
            x = max(0, x - padding)
            y = max(0, y - padding)
            w = min(img_array.shape[1] - x, w + 2 * padding)
            h = min(img_array.shape[0] - y, h + 2 * padding)
            
            # Crop
            cropped = img_array[y:y+h, x:x+w]
            
            return Image.fromarray(cropped)
            
        except Exception as e:
            logger.error(f"Pill region extraction error: {e}")
            return None
