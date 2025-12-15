from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Afiya Care"
    ENV: str = "development"
    DEBUG: bool = True
    API_VERSION: str = "v1"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 7860
    
    # Database
    DATABASE_URL: str
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    
    # Vector Database
    QDRANT_HOST: str
    QDRANT_PORT: int = 6333
    QDRANT_API_KEY: str
    QDRANT_HTTPS: bool = True
    QDRANT_COLLECTION: str = "medical_knowledge"
    
    # Authentication
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # N-ATLaS Configuration
    NATLAS_MODEL: str = "NCAIR1/N-ATLaS"
    NATLAS_MAX_LENGTH: int = 512        # Reduced from 2048
    NATLAS_MAX_NEW_TOKENS: int = 256    # Reduced from 512
    NATLAS_TEMPERATURE: float = 0.7
    NATLAS_TOP_P: float = 0.9
    
    # 🆕 Quantization settings
    NATLAS_USE_4BIT: bool = True        # Enable 4-bit quantization
    NATLAS_COMPUTE_DTYPE: str = "float16"
    
    # Embedding Model
    EMBEDDING_MODEL: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    MODEL_CACHE_DIR: str = "./models"
    
    # Redis
    REDIS_URL: str
    
    # Language Settings
    DEFAULT_LANGUAGE: str = "en"
    SUPPORTED_LANGUAGES: str = "en,yo,ha,ig,pcm"
    ENABLE_AUTO_LANGUAGE_DETECTION: bool = True
    
    # Safety & Compliance
    ENABLE_RED_FLAG_DETECTION: bool = True
    REQUIRE_DISCLAIMER: bool = True
    LOG_ANONYMIZATION: bool = True
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Monitoring
    ENABLE_METRICS: bool = True
    PROMETHEUS_PORT: int = 9090
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()