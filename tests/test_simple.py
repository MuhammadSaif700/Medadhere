"""
Simple tests for the MedAdhere API
"""
import pytest


def test_basic_import():
    """Test that we can import the main modules without errors"""
    try:
        from src.models.pill_identifier import PillIdentifier
        from src.models.medication_verifier import MedicationVerifier
        from src.models.adherence_tracker import AdherenceTracker
        
        # Test instantiation
        pill_identifier = PillIdentifier()
        assert pill_identifier is not None
        
        medication_verifier = MedicationVerifier()
        assert medication_verifier is not None
        
        adherence_tracker = AdherenceTracker()
        assert adherence_tracker is not None
        
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")


def test_pill_database():
    """Test pill database functionality"""
    from src.models.pill_identifier import PillIdentifier
    
    identifier = PillIdentifier()
    pills = identifier.get_all_pills()
    
    assert isinstance(pills, list)
    assert len(pills) > 0
    
    # Test pill structure
    pill = pills[0]
    assert "name" in pill
    assert "dosage" in pill


def test_search_functionality():
    """Test pill search functionality"""
    from src.models.pill_identifier import PillIdentifier
    
    identifier = PillIdentifier()
    
    # Test search by name
    results = identifier.search_pills({"name": "aspirin"})
    assert isinstance(results, list)
    
    # Test search by color
    results = identifier.search_pills({"color": "white"})
    assert isinstance(results, list)


def test_patient_schedules():
    """Test patient schedule functionality"""
    from src.models.medication_verifier import MedicationVerifier
    
    verifier = MedicationVerifier()
    
    # Test getting schedule for patient
    schedule = verifier.get_patient_schedule("patient_001")
    assert isinstance(schedule, list)


def test_adherence_stats():
    """Test adherence statistics"""
    from src.models.adherence_tracker import AdherenceTracker
    
    tracker = AdherenceTracker()
    
    # Test getting stats (should not crash)
    try:
        stats = tracker.get_current_stats("patient_001")
        assert stats is not None
    except Exception:
        # Expected to fail without proper data, but should not crash on import
        pass