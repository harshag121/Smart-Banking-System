"""
Banking Chatbot Config Module
Centralized configuration for easy management
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application Settings"""

    # API Configuration
    debug: bool = True
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_title: str = "Banking Chatbot API"
    api_version: str = "1.0.0"

    # CORS Configuration
    cors_origins: list = ["*"]
    cors_credentials: bool = True
    cors_methods: list = ["*"]
    cors_headers: list = ["*"]

    # Database Configuration (for future use)
    database_url: Optional[str] = None
    database_echo: bool = False

    # Session Configuration
    session_timeout: int = 3600  # 1 hour
    max_pending_transfers: int = 100

    # User Configuration
    demo_user_id: str = "user-123"
    demo_user_name: str = "John Demo"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Singleton instance
settings = Settings()
