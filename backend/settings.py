"""
Configuration avancée pour production
À utiliser avec les variables d'environnement
"""

import os
from functools import lru_cache

class Settings:
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost/stage_manager"
    )
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 heures
    
    # Admin
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "admin123")
    
    # Files
    EXCEL_FILE_PATH: str = os.getenv("EXCEL_FILE_PATH", "./fiches_stages.xlsx")
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50 MB
    
    # CORS
    ALLOWED_ORIGINS: list = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:8000"
    ).split(",")
    
    # API
    API_TITLE: str = "Stage Manager API"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
