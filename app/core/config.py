from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings and environment variables"""
    
    # API Settings
    APP_NAME: str = "MR & ASM Reporting Application"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Server Settings
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    
    # Database Settings
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/mr_reporting_db"
    DATABASE_ECHO: bool = False
    
    # JWT Settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS Settings
    ALLOWED_ORIGINS: list = ["*"]
    ALLOWED_CREDENTIALS: bool = True
    ALLOWED_METHODS: list = ["*"]
    ALLOWED_HEADERS: list = ["*"]
    
    # File Upload Settings
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_FILE_TYPES: list = ["pdf", "doc", "docx", "jpg", "jpeg", "png"]
    
    # Location Settings
    GEOFENCE_RADIUS_KM: float = 5.0
    
    # Email Settings (Optional)
    SMTP_SERVER: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
