from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict
from datetime import datetime

# Authentication Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Diagnosis Schemas
class DiagnosisRequest(BaseModel):
    symptoms: str = Field(..., min_length=10, max_length=1000)
    age: Optional[int] = Field(None, ge=0, le=150)
    gender: Optional[str] = Field(None, pattern="^(male|female|other)$")
    additional_info: Optional[str] = Field(None, max_length=500)
    language: Optional[str] = Field(
        None, 
        description="Language code (en, yo, ha, ig, pcm)"
    )

class ConditionMatch(BaseModel):
    title: str
    description: str
    symptoms: List[str]
    treatments: List[str]
    severity: str
    confidence: float

class DiagnosisResponse(BaseModel):
    conditions: List[ConditionMatch]
    red_flags: List[str]
    disclaimer: str
    response_id: str
    processing_time_ms: int
    recommendations: List[str]
    detected_language: Optional[str] = None
    natlas_analysis: Optional[str] = None

# Embedding Schemas
class EmbeddingRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000)
    language: Optional[str] = None

class EmbeddingResponse(BaseModel):
    embedding: List[float]
    dimension: int
    model_used: str

# Offline Sync Schemas
class OfflineSyncRequest(BaseModel):
    device_id: str
    pending_queries: List[DiagnosisRequest]
    client_kb_version: str
    last_sync_timestamp: Optional[datetime] = None

class OfflineSyncResponse(BaseModel):
    kb_update_required: bool
    kb_version: str
    processed_queries: List[DiagnosisResponse]
    sync_timestamp: datetime

# Admin Schemas
class MedicalConditionCreate(BaseModel):
    title: str
    symptoms: List[str]
    description: str
    treatments: List[str]
    red_flags: List[str]
    tags: List[str]
    severity_level: str

class KnowledgeBaseUpload(BaseModel):
    conditions: List[MedicalConditionCreate]

class KnowledgeBaseResponse(BaseModel):
    status: str
    conditions_added: int
    conditions_updated: int
    version: str
    timestamp: datetime