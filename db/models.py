from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, Float
from datetime import datetime
from core.database import Base

class User(Base):
    """User model for authentication"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MedicalCondition(Base):
    """Medical condition knowledge base"""
    __tablename__ = "medical_conditions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    symptoms = Column(JSON)
    description = Column(Text)
    treatments = Column(JSON)
    red_flags = Column(JSON)
    tags = Column(JSON)
    severity_level = Column(String)
    version = Column(String, default="1.0.0")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DiagnosisLog(Base):
    """Log of diagnosis requests"""
    __tablename__ = "diagnosis_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    session_id = Column(String, index=True)
    symptoms_text = Column(Text)
    detected_language = Column(String)
    matched_conditions = Column(JSON)
    red_flags_detected = Column(JSON)
    response_time_ms = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

class OfflineSync(Base):
    """Offline synchronization tracking"""
    __tablename__ = "offline_sync"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    device_id = Column(String, index=True)
    pending_queries = Column(JSON)
    client_kb_version = Column(String)
    synced_at = Column(DateTime, default=datetime.utcnow)
    sync_status = Column(String, default="pending")