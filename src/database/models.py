"""
Database models for MedAdhere system
"""
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base

class Patient(Base):
    """Patient information model"""
    __tablename__ = "patients"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    date_of_birth = Column(DateTime)
    email = Column(String)
    phone = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    medication_schedules = relationship("MedicationSchedule", back_populates="patient")
    dose_logs = relationship("DoseLog", back_populates="patient")
    adherence_reports = relationship("AdherenceReport", back_populates="patient")

class Medication(Base):
    """Medication information model"""
    __tablename__ = "medications"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    generic_name = Column(String)
    dosage = Column(String, nullable=False)
    shape = Column(String)
    color = Column(String)
    imprint = Column(String)
    size = Column(String)
    ndc_number = Column(String, unique=True)
    manufacturer = Column(String)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    schedules = relationship("MedicationSchedule", back_populates="medication")

class MedicationSchedule(Base):
    """Medication schedule model"""
    __tablename__ = "medication_schedules"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)
    medication_id = Column(Integer, ForeignKey("medications.id"), nullable=False)
    frequency = Column(String, nullable=False)  # e.g., "twice daily"
    times = Column(Text)  # JSON string of times
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    instructions = Column(Text)
    prescriber = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    patient = relationship("Patient", back_populates="medication_schedules")
    medication = relationship("Medication", back_populates="schedules")
    dose_logs = relationship("DoseLog", back_populates="schedule")

class DoseLog(Base):
    """Dose taking log model"""
    __tablename__ = "dose_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)
    schedule_id = Column(Integer, ForeignKey("medication_schedules.id"), nullable=False)
    scheduled_time = Column(DateTime, nullable=False)
    taken_time = Column(DateTime)
    status = Column(String, nullable=False)  # taken, missed, skipped
    confidence = Column(Float)  # AI confidence in detection
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    patient = relationship("Patient", back_populates="dose_logs")
    schedule = relationship("MedicationSchedule", back_populates="dose_logs")

class PillIdentification(Base):
    """Pill identification results model"""
    __tablename__ = "pill_identifications"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(String, ForeignKey("patients.id"))
    image_path = Column(String)
    identified_medication_id = Column(Integer, ForeignKey("medications.id"))
    confidence = Column(Float, nullable=False)
    features = Column(Text)  # JSON string of extracted features
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    patient = relationship("Patient")
    identified_medication = relationship("Medication")

class IngestionEvent(Base):
    """Ingestion detection events model"""
    __tablename__ = "ingestion_events"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)
    dose_log_id = Column(Integer, ForeignKey("dose_logs.id"))
    image_path = Column(String)
    detection_confidence = Column(Float, nullable=False)
    detected_actions = Column(Text)  # JSON string of detected actions
    is_confirmed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    patient = relationship("Patient")
    dose_log = relationship("DoseLog")

class AdherenceReport(Base):
    """Adherence reports model"""
    __tablename__ = "adherence_reports"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)
    report_period_start = Column(DateTime, nullable=False)
    report_period_end = Column(DateTime, nullable=False)
    overall_adherence_rate = Column(Float, nullable=False)
    total_scheduled_doses = Column(Integer, nullable=False)
    total_taken_doses = Column(Integer, nullable=False)
    missed_doses_count = Column(Integer, default=0)
    report_data = Column(Text)  # JSON string with detailed report data
    recommendations = Column(Text)  # JSON string with recommendations
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    patient = relationship("Patient", back_populates="adherence_reports")

class CaregiverContact(Base):
    """Caregiver contact information model"""
    __tablename__ = "caregiver_contacts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)
    name = Column(String, nullable=False)
    relationship_type = Column(String)  # son, daughter, spouse, etc.
    phone = Column(String)
    email = Column(String)
    is_primary = Column(Boolean, default=False)
    alert_preferences = Column(Text)  # JSON string with alert preferences
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    patient = relationship("Patient")

class Alert(Base):
    """Alert/notification model"""
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)
    caregiver_id = Column(Integer, ForeignKey("caregiver_contacts.id"))
    alert_type = Column(String, nullable=False)  # missed_dose, low_adherence, etc.
    severity = Column(String, nullable=False)  # low, medium, high, critical
    message = Column(Text, nullable=False)
    is_sent = Column(Boolean, default=False)
    sent_at = Column(DateTime)
    delivery_method = Column(String)  # sms, email, push
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    patient = relationship("Patient")
    caregiver = relationship("CaregiverContact")