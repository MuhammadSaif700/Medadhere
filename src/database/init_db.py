"""
Database initialization script
"""
from sqlalchemy import create_engine
from .database import Base, DATABASE_URL
from .models import *
import logging

logger = logging.getLogger(__name__)

def init_database():
    """Initialize the database with all tables"""
    try:
        # Create engine
        engine = create_engine(DATABASE_URL)
        
        # Drop all existing tables and recreate for fresh start
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        
        logger.info("Database initialized successfully with clean slate")
        print("✓ Database initialized with all tables (clean)")
        
        # Skip sample data seeding for clean start
        # seed_sample_data(engine)
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        print(f"✗ Error initializing database: {e}")
        raise

def seed_sample_data(engine):
    """Seed database with sample data for demonstration"""
    try:
        from sqlalchemy.orm import sessionmaker
        import json
        from datetime import datetime, time
        
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        
        # Check if data already exists
        if session.query(Patient).first():
            logger.info("Sample data already exists, skipping seeding")
            session.close()
            return
        
        # Create sample patient
        sample_patient = Patient(
            id="patient_001",
            name="John Doe",
            date_of_birth=datetime(1960, 5, 15),
            email="john.doe@email.com",
            phone="+1-555-0123"
        )
        session.add(sample_patient)
        
        # Create sample medications
        aspirin = Medication(
            name="Aspirin",
            generic_name="Acetylsalicylic Acid",
            dosage="325mg",
            shape="round",
            color="white",
            imprint="BAYER",
            size="standard",
            ndc_number="12345-678-90",
            manufacturer="Bayer",
            description="Pain reliever and blood thinner"
        )
        
        ibuprofen = Medication(
            name="Ibuprofen",
            generic_name="Ibuprofen",
            dosage="200mg",
            shape="oval",
            color="brown",
            imprint="I-2",
            size="standard",
            ndc_number="98765-432-10",
            manufacturer="Generic",
            description="Anti-inflammatory pain reliever"
        )
        
        session.add_all([aspirin, ibuprofen])
        session.commit()  # Commit to get IDs
        
        # Create sample medication schedules
        aspirin_schedule = MedicationSchedule(
            patient_id="patient_001",
            medication_id=aspirin.id,
            frequency="once daily",
            times=json.dumps(["08:00"]),
            start_date=datetime(2024, 1, 1),
            instructions="Take with food",
            prescriber="Dr. Smith"
        )
        
        ibuprofen_schedule = MedicationSchedule(
            patient_id="patient_001",
            medication_id=ibuprofen.id,
            frequency="twice daily",
            times=json.dumps(["08:00", "20:00"]),
            start_date=datetime(2024, 1, 1),
            instructions="Take with water",
            prescriber="Dr. Smith"
        )
        
        session.add_all([aspirin_schedule, ibuprofen_schedule])
        
        # Create sample caregiver contact
        caregiver = CaregiverContact(
            patient_id="patient_001",
            name="Jane Doe",
            relationship_type="daughter",
            phone="+1-555-0124",
            email="jane.doe@email.com",
            is_primary=True,
            alert_preferences=json.dumps({
                "missed_dose": True,
                "low_adherence": True,
                "method": "both"
            })
        )
        session.add(caregiver)
        
        session.commit()
        session.close()
        
        logger.info("Sample data seeded successfully")
        print("✓ Sample data seeded successfully")
        
    except Exception as e:
        logger.error(f"Error seeding sample data: {e}")
        print(f"✗ Error seeding sample data: {e}")

if __name__ == "__main__":
    init_database()