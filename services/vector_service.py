from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from typing import List, Dict, Optional
from core.config import settings
import uuid

class VectorService:
    """Vector database service using Qdrant"""
    
    def __init__(self):
        self.client = None
        
    async def initialize(self):
        """Initialize Qdrant client and create collection"""
        print(f"🔗 Connecting to Qdrant at {settings.QDRANT_HOST}:{settings.QDRANT_PORT}")
        
        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
            timeout=30
        )
        
        # Create collection if it doesn't exist
        try:
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]
            
            if settings.QDRANT_COLLECTION not in collection_names:
                self.client.create_collection(
                    collection_name=settings.QDRANT_COLLECTION,
                    vectors_config=VectorParams(
                        size=384,  # all-MiniLM-L6-v2 dimension
                        distance=Distance.COSINE
                    )
                )
                print(f"✅ Created Qdrant collection: {settings.QDRANT_COLLECTION}")
            else:
                print(f"✅ Qdrant collection exists: {settings.QDRANT_COLLECTION}")
                
        except Exception as e:
            print(f"❌ Error initializing Qdrant: {e}")
            raise
    
    async def insert(
        self, 
        embeddings: List[List[float]], 
        payloads: List[Dict]
    ) -> int:
        """Insert embeddings with metadata"""
        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload=payload
            )
            for embedding, payload in zip(embeddings, payloads)
        ]
        
        result = self.client.upsert(
            collection_name=settings.QDRANT_COLLECTION,
            points=points
        )
        
        return len(points)
    
    async def search(
        self, 
        query_embedding: List[float], 
        top_k: int = 5,
        filters: Optional[Dict] = None
    ) -> List[Dict]:
        """Search for similar vectors"""
        
        # Build filter if provided
        search_filter = None
        if filters:
            conditions = []
            for key, value in filters.items():
                conditions.append(
                    FieldCondition(
                        key=key,
                        match=MatchValue(value=value)
                    )
                )
            search_filter = Filter(must=conditions)
        
        results = self.client.search(
            collection_name=settings.QDRANT_COLLECTION,
            query_vector=query_embedding,
            limit=top_k,
            query_filter=search_filter
        )
        
        return [
            {
                "id": result.id,
                "score": result.score,
                "payload": result.payload
            }
            for result in results
        ]
    
    async def delete_by_id(self, point_id: str):
        """Delete a point by ID"""
        self.client.delete(
            collection_name=settings.QDRANT_COLLECTION,
            points_selector=[point_id]
        )
    
    async def get_collection_info(self) -> Dict:
        """Get collection information"""
        info = self.client.get_collection(settings.QDRANT_COLLECTION)
        return {
            "vectors_count": info.vectors_count,
            "points_count": info.points_count,
            "status": info.status
        }
    
    async def close(self):
        """Close the client connection"""
        if self.client:
            self.client.close()
            print("✅ Qdrant connection closed")