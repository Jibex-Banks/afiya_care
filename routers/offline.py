from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from datetime import datetime

from core.database import get_db
from db.schemas import OfflineSyncRequest, OfflineSyncResponse
from db.models import OfflineSync

router = APIRouter()
KB_VERSION = "1.0.0"

@router.post("/sync", response_model=OfflineSyncResponse)
async def sync_offline_data(request: OfflineSyncRequest, req: Request, db: Session = Depends(get_db)):
    """Sync offline data"""
    from routers.diagnose import diagnose_symptoms
    
    processed = []
    for query in request.pending_queries:
        try:
            result = await diagnose_symptoms(query, req, db)
            processed.append(result)
        except:
            continue
    
    sync_log = OfflineSync(
        device_id=request.device_id,
        pending_queries=[q.dict() for q in request.pending_queries],
        client_kb_version=request.client_kb_version,
        sync_status="completed"
    )
    db.add(sync_log)
    db.commit()
    
    return OfflineSyncResponse(
        kb_update_required=request.client_kb_version != KB_VERSION,
        kb_version=KB_VERSION,
        processed_queries=processed,
        sync_timestamp=datetime.utcnow()
    )