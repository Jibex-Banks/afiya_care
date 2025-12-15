from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import datetime

from core.database import get_db
from core.security import verify_token
from db.schemas import KnowledgeBaseUpload, KnowledgeBaseResponse
from db.models import User, MedicalCondition

router = APIRouter()

def verify_admin(user_id: str = Depends(verify_token), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin required")
    return user

@router.post("/upload-kb", response_model=KnowledgeBaseResponse)
async def upload_kb(kb_data: KnowledgeBaseUpload, req: Request, db: Session = Depends(get_db), admin: User = Depends(verify_admin)):
    """Upload knowledge base"""
    try:
        from app.services.ml_service import MLService
        from app.services.vector_service import VectorService
        
        ml_service: MLService = req.app.state.ml_service
        vector_service: VectorService = req.app.state.vector_service
        
        added, updated = 0, 0
        version = f"1.0.{int(datetime.utcnow().timestamp())}"
        
        texts, condition_objs = [], []
        
        for cond in kb_data.conditions:
            existing = db.query(MedicalCondition).filter(MedicalCondition.title == cond.title).first()
            
            if existing:
                existing.symptoms = cond.symptoms
                existing.description = cond.description
                existing.treatments = cond.treatments
                existing.version = version
                updated += 1
                cond_obj = existing
            else:
                cond_obj = MedicalCondition(**cond.dict(), version=version)
                db.add(cond_obj)
                added += 1
            
            texts.append(f"{cond.title}. {', '.join(cond.symptoms)}. {cond.description}")
            condition_objs.append(cond_obj)
        
        db.commit()
        
        embeddings = await ml_service.generate_embeddings_batch(texts)
        payloads = [
            {
                "condition_id": c.id,
                "title": c.title,
                "symptoms": c.symptoms,
                "description": c.description,
                "treatments": c.treatments,
                "severity_level": c.severity_level
            }
            for c in condition_objs
        ]
        
        await vector_service.insert(embeddings, payloads)
        
        return KnowledgeBaseResponse(
            status="success",
            conditions_added=added,
            conditions_updated=updated,
            version=version,
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))