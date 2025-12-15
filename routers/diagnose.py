from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import time
import uuid
from typing import List

from core.database import get_db
from db.schemas import DiagnosisRequest, DiagnosisResponse, ConditionMatch
from services.ml_service import MLService
from services.vector_service import VectorService
from services.safety_service import SafetyService
from db.models import DiagnosisLog

router = APIRouter()

@router.post("/diagnose", response_model=DiagnosisResponse)
async def diagnose_symptoms(request: DiagnosisRequest, req: Request, db: Session = Depends(get_db)):
    """🇳🇬 N-ATLaS powered diagnosis - Supports EN, YO, HA, IG, PCM"""
    start_time = time.time()
    session_id = str(uuid.uuid4())
    
    try:
        ml_service: MLService = req.app.state.ml_service
        vector_service: VectorService = req.app.state.vector_service
        safety_service = SafetyService()
        
        # Detect language
        detected_lang = request.language or ml_service.detect_language(request.symptoms)
        print(f"🌍 Language: {detected_lang}")
        
        # N-ATLaS analysis
        natlas_analysis = await ml_service.analyze_with_natlas(request.symptoms, detected_lang)
        
        # Generate embedding
        embedding = await ml_service.generate_embedding(request.symptoms)
        
        # Search knowledge base
        search_results = await vector_service.search(embedding, top_k=5)
        
        # Check red flags
        red_flags = safety_service.detect_red_flags(request.symptoms, detected_lang)
        
        # Format conditions
        conditions: List[ConditionMatch] = []
        for result in search_results:
            p = result["payload"]
            conditions.append(ConditionMatch(
                title=p.get("title", "Unknown"),
                description=p.get("description", ""),
                symptoms=p.get("symptoms", []),
                treatments=p.get("treatments", []),
                severity=p.get("severity_level", "moderate"),
                confidence=round(result["score"], 3)
            ))
        
        recommendations = safety_service.get_recommendations(red_flags)
        disclaimer = safety_service.get_disclaimer(detected_lang)
        processing_time = int((time.time() - start_time) * 1000)
        
        # Log
        log = DiagnosisLog(
            session_id=session_id,
            symptoms_text=request.symptoms[:100],
            detected_language=detected_lang,
            matched_conditions=[c.title for c in conditions],
            red_flags_detected=[f["category"] for f in red_flags],
            response_time_ms=processing_time
        )
        db.add(log)
        db.commit()
        
        return DiagnosisResponse(
            conditions=conditions,
            red_flags=[f["message"] for f in red_flags],
            disclaimer=disclaimer,
            response_id=session_id,
            processing_time_ms=processing_time,
            recommendations=recommendations,
            detected_language=detected_lang,
            natlas_analysis=natlas_analysis[:200]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/languages")
async def get_supported_languages(req: Request):
    """Get supported languages"""
    ml_service: MLService = req.app.state.ml_service
    return ml_service.get_model_info()["natlas"]["supported_languages"]