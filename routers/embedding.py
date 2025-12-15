from fastapi import APIRouter, Request, HTTPException
from db.schemas import EmbeddingRequest, EmbeddingResponse

router = APIRouter()

@router.post("/embedding", response_model=EmbeddingResponse)
async def generate_embedding(request: EmbeddingRequest, req: Request):
    """Generate embedding"""
    try:
        from services.ml_service import MLService
        ml_service: MLService = req.app.state.ml_service
        
        embedding = await ml_service.generate_embedding(request.text, request.language)
        
        return EmbeddingResponse(
            embedding=embedding,
            dimension=len(embedding),
            model_used=ml_service.get_model_info()["embedding_model"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))