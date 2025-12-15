from sentence_transformers import SentenceTransformer
from typing import List, Optional
import torch
from core.config import settings
from services.natlas_service import NATLaSService

class MLService:
    """ML Service with N-ATLaS and embeddings"""
    
    def __init__(self):
        self.embedding_model = None
        self.natlas_service = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    async def initialize(self):
        """Initialize all ML services"""
        print(f"🤖 Initializing ML Services on {self.device}")
        
        # Load embedding model
        print(f"📊 Loading: {settings.EMBEDDING_MODEL}")
        self.embedding_model = SentenceTransformer(
            settings.EMBEDDING_MODEL,
            device=self.device
        )
        print("✅ Embedding model loaded")
        
        # Initialize N-ATLaS
        self.natlas_service = NATLaSService()
        await self.natlas_service.initialize()
    
    async def generate_embedding(self, text: str, language: Optional[str] = None) -> List[float]:
        """Generate embedding"""
        if self.embedding_model is None:
            raise RuntimeError("Embedding model not initialized")
        
        embedding = self.embedding_model.encode(
            text.strip(),
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        return embedding.tolist()
    
    async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings in batch"""
        if self.embedding_model is None:
            raise RuntimeError("Embedding model not initialized")
        
        embeddings = self.embedding_model.encode(
            [t.strip() for t in texts],
            convert_to_numpy=True,
            batch_size=32,
            normalize_embeddings=True
        )
        return embeddings.tolist()
    
    async def analyze_with_natlas(self, symptoms: str, language: str = "en") -> str:
        """Use N-ATLaS for analysis"""
        return await self.natlas_service.analyze_symptoms(symptoms, language)
    
    def detect_language(self, text: str) -> str:
        """Detect language"""
        return self.natlas_service.detect_language(text)
    
    def get_model_info(self) -> dict:
        """Get model information"""
        return {
            "embedding_model": settings.EMBEDDING_MODEL,
            "device": self.device,
            "dimension": self.embedding_model.get_sentence_embedding_dimension(),
            "natlas": self.natlas_service.get_model_info()
        }