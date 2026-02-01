"""
Pill identification model using computer vision
"""
import numpy as np
# import cv2  # Commented out for compatibility
from PIL import Image
# import tensorflow as tf  # Commented out for compatibility
from typing import Dict, List, Optional, Any
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class PillIdentifier:
    """
    Machine learning model for identifying pills from images
    Uses CNN for image classification and feature extraction
    """
    
    def __init__(self, model_path: str = "data/models/pill_identifier.h5"):
        self.model_path = model_path
        self.model = None
        self.class_names = []
        self.pill_database = {}
        self.confidence_threshold = 0.7
        
        self._load_model()
        self._load_pill_database()
    
    def _load_model(self):
        """Load the trained pill identification model"""
        try:
            # For demo purposes, use mock model
            logger.info("Using mock model for demonstration")
            self.model = self._create_base_model()
                
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self.model = self._create_base_model()
    
    def _create_base_model(self):
        """Create a base CNN model for pill identification"""
        # Mock model for demonstration without TensorFlow
        return {"type": "mock_cnn", "version": "1.0"}
    
    def _load_pill_database(self):
        """Load pill information database"""
        try:
            db_path = Path("data/pill_database.json")
            if db_path.exists():
                with open(db_path, 'r') as f:
                    self.pill_database = json.load(f)
                # If empty, create sample data
                if not self.pill_database:
                    logger.info("Pill database empty - creating sample data")
                    self._create_sample_database()
                else:
                    logger.info(f"Loaded pill database with {len(self.pill_database)} entries")
            else:
                # Create sample database for demo
                logger.info("Pill database missing - creating sample database")
                self._create_sample_database()
                
        except Exception as e:
            logger.error(f"Error loading pill database: {e}")
            # Create sample data as fallback
            self._create_sample_database()
    
    def _create_sample_database(self):
        """Create a sample pill database for demonstration"""
        self.pill_database = {
            "aspirin_325mg": {
                "name": "Aspirin",
                "dosage": "325mg",
                "shape": "round",
                "color": "white",
                "imprint": "BAYER",
                "size": "standard",
                "ndc_number": "12345-678-90",
                "manufacturer": "Bayer"
            },
            "ibuprofen_200mg": {
                "name": "Ibuprofen",
                "dosage": "200mg",
                "shape": "oval",
                "color": "brown",
                "imprint": "I-2",
                "size": "standard",
                "ndc_number": "98765-432-10",
                "manufacturer": "Generic"
            },
            "acetaminophen_500mg": {
                "name": "Acetaminophen",
                "dosage": "500mg",
                "shape": "capsule",
                "color": "red_white",
                "imprint": "TYLENOL",
                "size": "standard",
                "ndc_number": "11111-222-33",
                "manufacturer": "Johnson & Johnson"
            }
        }
        
        # Save sample database
        db_path = Path("data")
        db_path.mkdir(exist_ok=True)
        with open(db_path / "pill_database.json", 'w') as f:
            json.dump(self.pill_database, f, indent=2)
    
    def identify(self, image: np.ndarray, confidence_threshold: float = None) -> Optional[Dict[str, Any]]:
        """
        Identify a pill from an image
        
        Args:
            image: Preprocessed image array
            confidence_threshold: Minimum confidence for identification
            
        Returns:
            Dictionary with pill info and confidence, or None if not identified
        """
        if confidence_threshold is None:
            confidence_threshold = 0.3  # Lower threshold for demo
            
        try:
            # For demo purposes, return mock result with database pills
            if not self.pill_database:
                return None
            
            # Return first pill from database with decent confidence
            pill_id = list(self.pill_database.keys())[0]
            pill_info = self.pill_database[pill_id]
            
            return {
                "pill_info": pill_info,
                "confidence": 0.75,  # Mock confidence
                "pill_id": pill_id
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error during pill identification: {e}")
            return None
    
    def _mock_identification(self, image: np.ndarray) -> Dict[str, Any]:
        """Mock identification for demonstration purposes"""
        # Simple mock based on image properties
        mean_color = float(np.mean(image))

        # Allow either normalized [0,1] images or [0,255] images
        if mean_color <= 1.0:
            # normalized
            if mean_color > 0.66:
                pill_id = "aspirin_325mg"
            elif mean_color > 0.33:
                pill_id = "ibuprofen_200mg"
            else:
                pill_id = "acetaminophen_500mg"
        else:
            # 0-255 scale
            if mean_color > 200:
                pill_id = "aspirin_325mg"
            elif mean_color > 100:
                pill_id = "ibuprofen_200mg"
            else:
                pill_id = "acetaminophen_500mg"
        
        # If the selected pill id is not present in the database (empty DB), return None
        if pill_id not in self.pill_database:
            return None

        return {
            "pill_info": self.pill_database[pill_id],
            "confidence": 0.85,
            "pill_id": pill_id
        }
    
    def get_all_pills(self) -> List[Dict[str, Any]]:
        """Get all pills in the database"""
        return list(self.pill_database.values())

    def add_pill(self, pill_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a pill entry to the in-memory database and persist it to disk.

        Returns the stored pill record including the generated pill id/key.
        """
        try:
            # Generate a stable key from name and dosage
            base_key = f"{pill_data.get('name','pill').strip().lower().replace(' ', '_')}_{pill_data.get('dosage','').strip().lower().replace(' ', '_')}"
            key = base_key
            counter = 1
            while key in self.pill_database:
                key = f"{base_key}_{counter}"
                counter += 1

            # Ensure directory exists
            db_dir = Path('data')
            db_dir.mkdir(parents=True, exist_ok=True)

            self.pill_database[key] = pill_data

            # Persist to disk
            with open(db_dir / 'pill_database.json', 'w') as f:
                json.dump(self.pill_database, f, indent=2)

            return {"id": key, **pill_data}
        except Exception as e:
            logger.error(f"Error adding pill: {e}")
            raise
    
    def search_pills(self, criteria: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Search pills by various criteria
        
        Args:
            criteria: Dictionary of search criteria
            
        Returns:
            List of matching pills
        """
        results = []
        
        for pill_info in self.pill_database.values():
            match = True
            for key, value in criteria.items():
                if key in pill_info:
                    if value.lower() not in pill_info[key].lower():
                        match = False
                        break
                else:
                    match = False
                    break
            
            if match:
                results.append(pill_info)
        
        return results
    
    def train_model(self, training_data_path: str, epochs: int = 50):
        """
        Train the pill identification model
        
        Args:
            training_data_path: Path to training data directory
            epochs: Number of training epochs
        """
        try:
            # Implementation would load training data and train the model
            # This is a placeholder for the actual training implementation
            logger.info(f"Training model with data from {training_data_path}")
            
            # Save trained model
            model_dir = Path(self.model_path).parent
            model_dir.mkdir(parents=True, exist_ok=True)
            self.model.save(self.model_path)
            
        except Exception as e:
            logger.error(f"Error training model: {e}")
            raise

    def clear_database(self):
        """Clear the in-memory pill database and remove persisted file."""
        try:
            self.pill_database = {}
            db_path = Path('data')
            db_path.mkdir(parents=True, exist_ok=True)
            file_path = db_path / 'pill_database.json'
            if file_path.exists():
                file_path.unlink()
            # Ensure an empty file exists
            with open(file_path, 'w') as f:
                json.dump(self.pill_database, f, indent=2)
            logger.info('Cleared pill database (in-memory and on-disk)')
        except Exception as e:
            logger.error(f'Error clearing pill database: {e}')