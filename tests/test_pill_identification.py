"""
Tests for pill identification functionality
"""
import pytest
import numpy as np
from PIL import Image
import io
import base64

from src.models.pill_identifier import PillIdentifier
from src.vision.image_processor import ImageProcessor

class TestPillIdentifier:
    """Test cases for PillIdentifier class"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.pill_identifier = PillIdentifier()
        self.image_processor = ImageProcessor()
    
    def test_pill_identifier_initialization(self):
        """Test pill identifier initialization"""
        assert self.pill_identifier is not None
        assert self.pill_identifier.pill_database is not None
        assert len(self.pill_identifier.pill_database) > 0
    
    def test_get_all_pills(self):
        """Test getting all pills from database"""
        pills = self.pill_identifier.get_all_pills()
        assert isinstance(pills, list)
        assert len(pills) > 0
        
        # Check pill structure
        pill = pills[0]
        required_fields = ["name", "dosage", "shape", "color"]
        for field in required_fields:
            assert field in pill
    
    def test_search_pills(self):
        """Test searching pills by criteria"""
        # Search by name
        results = self.pill_identifier.search_pills({"name": "aspirin"})
        assert isinstance(results, list)
        
        # Search by color
        results = self.pill_identifier.search_pills({"color": "white"})
        assert isinstance(results, list)
    
    def test_mock_identification(self):
        """Test mock pill identification"""
        # Create a test image
        test_image = np.random.rand(224, 224, 3)
        
        result = self.pill_identifier._mock_identification(test_image)
        assert result is not None
        assert "pill_info" in result
        assert "confidence" in result
        assert "pill_id" in result
        assert isinstance(result["confidence"], (int, float))
        assert 0 <= result["confidence"] <= 1

class TestImageProcessor:
    """Test cases for ImageProcessor class"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.processor = ImageProcessor()
    
    def create_test_image(self, size=(224, 224), color=(255, 255, 255)):
        """Create a test PIL image"""
        return Image.new("RGB", size, color)
    
    def test_preprocess_for_identification(self):
        """Test image preprocessing for identification"""
        test_image = self.create_test_image()
        processed = self.processor.preprocess_for_identification(test_image)
        
        assert isinstance(processed, np.ndarray)
        assert processed.shape == (224, 224, 3)
        assert processed.dtype == np.float32
        assert np.all(processed >= 0) and np.all(processed <= 1)
    
    def test_enhance_image(self):
        """Test image enhancement"""
        test_image = self.create_test_image()
        enhanced = self.processor._enhance_image(test_image)
        
        assert isinstance(enhanced, Image.Image)
        assert enhanced.size == test_image.size
    
    def test_extract_pill_features(self):
        """Test pill feature extraction"""
        test_image = self.create_test_image()
        features = self.processor.extract_pill_features(test_image)
        
        assert isinstance(features, dict)
        # Check for expected feature categories
        expected_categories = ["dominant_color", "shape_metrics"]
        for category in expected_categories:
            if category in features:
                assert features[category] is not None
    
    def test_dominant_color_detection(self):
        """Test dominant color detection"""
        # Create image with known color
        red_image = self.create_test_image(color=(255, 0, 0))
        color = self.processor._get_dominant_color(red_image)
        
        assert isinstance(color, tuple)
        assert len(color) == 3
        assert all(isinstance(c, (int, np.integer)) for c in color)
    
    def test_preprocess_for_ingestion(self):
        """Test image preprocessing for ingestion detection"""
        test_image = self.create_test_image()
        processed = self.processor.preprocess_for_ingestion(test_image)
        
        assert isinstance(processed, np.ndarray)
        assert processed.shape == (224, 224, 3)
        assert processed.dtype == np.float32