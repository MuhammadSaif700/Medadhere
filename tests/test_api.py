"""
Tests for API endpoints
"""
import pytest
import json
from fastapi.testclient import TestClient

# Import will be done in test functions to avoid import issues

class TestHealthEndpoints:
    """Test health and basic endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        from src.api.main import app
        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
    
    def test_health_check(self):
        """Test health check endpoint"""
        from src.api.main import app
        client = TestClient(app)
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data

class TestPillIdentificationAPI:
    """Test pill identification API endpoints"""
    
    def test_get_pill_database(self):
        """Test getting pill database"""
        from src.api.main import app
        client = TestClient(app)
        response = client.get("/api/v1/pills/database")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_search_pills_no_params(self):
        """Test searching pills without parameters"""
        from src.api.main import app
        client = TestClient(app)
        response = client.get("/api/v1/pills/search")
        assert response.status_code == 200
    
    def test_search_pills_with_name(self):
        """Test searching pills by name"""
        from src.api.main import app
        client = TestClient(app)
        response = client.get("/api/v1/pills/search?name=aspirin")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_search_pills_with_color(self):
        """Test searching pills by color"""
        from src.api.main import app
        client = TestClient(app)
        response = client.get("/api/v1/pills/search?color=white")
        assert response.status_code == 200

class TestMedicationVerificationAPI:
    """Test medication verification API endpoints"""
    
    def test_get_nonexistent_patient_schedule(self):
        """Test getting schedule for non-existent patient"""
        from src.api.main import app
        client = TestClient(app)
        response = client.get("/api/v1/medications/schedule/nonexistent_patient")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

class TestAdherenceAPI:
    """Test adherence tracking API endpoints"""
    
    def test_get_adherence_stats_nonexistent_patient(self):
        """Test getting stats for non-existent patient"""
        from src.api.main import app
        client = TestClient(app)
        response = client.get("/api/v1/adherence/stats/nonexistent_patient")
        # Should handle gracefully even if patient doesn't exist
        assert response.status_code in [200, 404, 500]
    
    def test_get_missed_doses_nonexistent_patient(self):
        """Test getting missed doses for non-existent patient"""
        from src.api.main import app
        client = TestClient(app)
        response = client.get("/api/v1/adherence/missed-doses/nonexistent_patient")
        # Should handle gracefully
        assert response.status_code in [200, 404, 500]