"""
Simplified image processing utilities for pill identification
"""
import numpy as np
from PIL import Image, ImageEnhance
from typing import Tuple, Optional, List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class ImageProcessor:
    """
    Simplified image processor for pill identification without OpenCV dependencies
    """
    
    def __init__(self):
        self.target_size = (224, 224)
        self.enhancement_factor = 1.2
    
    def preprocess_for_identification(self, image: Image.Image) -> np.ndarray:
        """
        Preprocess image for pill identification
        
        Args:
            image: PIL Image object
            
        Returns:
            Preprocessed image as numpy array
        """
        try:
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize to target size
            resized_image = image.resize(self.target_size, Image.Resampling.LANCZOS)
            
            # Convert to numpy array and normalize
            image_array = np.array(resized_image, dtype=np.float32) / 255.0
            
            return image_array
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {e}")
            return np.zeros((*self.target_size, 3), dtype=np.float32)
    
    def preprocess_for_ingestion(self, image: Image.Image) -> np.ndarray:
        """
        Preprocess image for ingestion detection
        
        Args:
            image: PIL Image object
            
        Returns:
            Preprocessed image as numpy array
        """
        return self.preprocess_for_identification(image)
    
    def extract_pill_features(self, image: Image.Image) -> Dict[str, Any]:
        """
        Extract basic features from pill image
        
        Args:
            image: PIL Image of the pill
            
        Returns:
            Dictionary containing extracted features
        """
        try:
            features = {}
            
            # Convert to numpy array
            img_array = np.array(image)
            
            # Basic features
            features.update({
                "dominant_color": self._get_dominant_color(image),
                "image_dimensions": {
                    "width": image.width,
                    "height": image.height,
                    "aspect_ratio": image.width / image.height if image.height > 0 else 0
                },
                "brightness": float(np.mean(img_array)),
                "contrast": float(np.std(img_array))
            })
            
            # Color channel analysis
            if len(img_array.shape) == 3:
                features["color_channels"] = {
                    "red_mean": float(np.mean(img_array[:, :, 0])),
                    "green_mean": float(np.mean(img_array[:, :, 1])),
                    "blue_mean": float(np.mean(img_array[:, :, 2]))
                }
            
            return features
            
        except Exception as e:
            logger.error(f"Error extracting features: {e}")
            return {"error": f"Feature extraction failed: {str(e)}"}
    
    def _get_dominant_color(self, image: Image.Image) -> Tuple[int, int, int]:
        """
        Get dominant color from image using simple averaging
        
        Args:
            image: PIL Image
            
        Returns:
            RGB tuple of dominant color
        """
        try:
            # Resize for faster processing
            small_image = image.resize((50, 50))
            
            # Convert to numpy and get average color
            img_array = np.array(small_image)
            if len(img_array.shape) == 3:
                dominant_color = np.mean(img_array.reshape(-1, 3), axis=0)
                return tuple(map(int, dominant_color))
            else:
                # Grayscale
                avg_value = int(np.mean(img_array))
                return (avg_value, avg_value, avg_value)
                
        except Exception as e:
            logger.error(f"Error getting dominant color: {e}")
            return (128, 128, 128)  # Default gray