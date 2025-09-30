"""
Test configuration and fixtures
"""
import pytest
import tempfile
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from src.database.database import Base, get_db
from src.api.main import app

# Test database setup
@pytest.fixture
def test_db():
    """Create test database"""
    # Create temporary database file
    db_fd, db_path = tempfile.mkstemp()
    database_url = f"sqlite:///{db_path}"
    
    engine = create_engine(database_url, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield TestingSessionLocal
    
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(test_db):
    """Create test client"""
    return TestClient(app)

@pytest.fixture
def sample_patient_data():
    """Sample patient data for testing"""
    return {
        "id": "test_patient_001",
        "name": "Test Patient",
        "email": "test@example.com",
        "phone": "+1-555-0123"
    }

@pytest.fixture
def sample_medication_data():
    """Sample medication data for testing"""
    return {
        "name": "Test Medication",
        "dosage": "100mg",
        "shape": "round",
        "color": "white",
        "ndc_number": "12345-678-90"
    }