from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from prometheus_client import make_asgi_app

from core.config import settings
from core.database import engine, Base
from routers import diagnose, embedding, offline, admin, auth
from services.ml_service import MLService
from services.vector_service import VectorService

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("=" * 60)
    print("🚀 Starting Afiya Care Backend with N-ATLaS")
    print("=" * 60)
    
    # Initialize database tables
    print("📊 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
    
    # Initialize ML service (includes N-ATLaS)
    print("🤖 Initializing ML Services...")
    app.state.ml_service = MLService()
    await app.state.ml_service.initialize()
    print("✅ ML Services initialized")
    
    # Initialize vector service
    print("💾 Initializing Vector Database...")
    app.state.vector_service = VectorService()
    await app.state.vector_service.initialize()
    print("✅ Vector Database initialized")
    
    print("=" * 60)
    print("✅ Afiya Care Backend Ready!")
    print(f"📚 API Docs: http://localhost:{settings.PORT}/docs")
    print(f"🌍 N-ATLaS Languages: Yoruba, Hausa, Igbo, Pidgin, English")
    print("=" * 60)
    
    yield
    
    # Shutdown
    print("\n🛑 Shutting down services...")
    await app.state.vector_service.close()
    print("✅ Shutdown complete")

# Get port from environment (HF Spaces uses 7860)
PORT = settings.PORT

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered medical assistance with N-ATLaS multilingual support",
    version=settings.API_VERSION,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Include routers
app.include_router(auth.router, prefix=f"/api/{settings.API_VERSION}/auth", tags=["Authentication"])
app.include_router(diagnose.router, prefix=f"/api/{settings.API_VERSION}", tags=["Diagnosis"])
app.include_router(embedding.router, prefix=f"/api/{settings.API_VERSION}", tags=["Embeddings"])
app.include_router(offline.router, prefix=f"/api/{settings.API_VERSION}/offline", tags=["Offline Sync"])
app.include_router(admin.router, prefix=f"/api/{settings.API_VERSION}/admin", tags=["Admin"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Afiya Care API",
        "version": settings.API_VERSION,
        "model": "N-ATLaS (NCAIR1/N-ATLaS)",
        "languages": ["English", "Yoruba", "Hausa", "Igbo", "Nigerian Pidgin"],
        "status": "operational",
        "docs": f"/docs"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "ml_service": "ready",
        "natlas": "ready",
        "vector_db": "ready"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)