"""
Configuration module.

Provides application settings following:
- "Explicit is better than implicit"
- "Simple is better than complex"
"""
import os
from enum import Enum
from typing import List, Optional, Dict, Any
from functools import lru_cache

from pydantic import field_validator, Field, model_validator
from pydantic_settings import BaseSettings


class LogLevel(str, Enum):
    """Valid logging levels - explicit enumeration makes valid options clear."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING" 
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Environment(str, Enum):
    """Application environment types - explicit enumeration of valid environments."""
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """
    Application settings with explicit typing and defaults.
    
    Follows "Explicit is better than implicit" by clearly defining
    all configuration options with types and defaults.
    """
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Wedding RSVP API"
    
    # Environment settings
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    DEBUG: bool = Field(default=False, description="Enable debug mode")
    LOG_LEVEL: LogLevel = LogLevel.INFO
    
    # Path settings - explicit paths make configuration clearer
    BASE_DIR: str = Field(
        default="",
        description="Base directory of the application"
    )
    FRONTEND_PATH: Optional[str] = Field(
        default=None,
        description="Path to frontend build directory"
    )
    
    # Security settings
    ALLOWED_ORIGINS: List[str] = Field(
        default=["*"],
        description="CORS allowed origins"
    )
    
    # Database settings
    DATABASE_URI: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/wedding_rsvp",
        description="Database connection URI"
    )
    
    # SQLAlchemy settings
    SQL_ECHO: bool = Field(
        default=False,
        description="Enable SQLAlchemy query logging"
    )
    
    # WhatsApp settings
    WHATSAPP_VERIFY_TOKEN: str = Field(
        default="your_verify_token_here",
        description="WhatsApp API verification token"
    )
    
    # File-based configuration
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "ignore",
    }
    
    # Explicit validation makes the code more readable
    @field_validator("BASE_DIR", mode="before")
    def set_base_dir(cls, v: str) -> str:
        """Set base directory if not provided."""
        if not v:
            # Two levels up from this file (app/backend/core/config.py)
            return os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        return v
    
    @field_validator("FRONTEND_PATH", mode="before")
    def set_frontend_path(cls, v: Optional[str], info) -> str:
        """Set frontend path relative to BASE_DIR if not provided."""
        if v is not None:
            return v
            
        # Get the base directory from values
        base_dir = info.data.get("BASE_DIR", "")
        if not base_dir:
            # Fallback to calculating it
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            
        # Frontend is expected to be at app/frontend/build
        return os.path.join(base_dir, "frontend", "build")
    
    def MODEL_DUMP_JSON(self, **kwargs) -> str:
        """Custom JSON dumping method that handles Enums properly."""
        import json
        
        data = self.model_dump()
        # Convert enums to strings for JSON serialization
        for key, value in data.items():
            if isinstance(value, Enum):
                data[key] = value.value
                
        return json.dumps(data, **kwargs)


@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings, using caching for efficiency.
    
    Simple function that follows "Simple is better than complex" principle
    by having a single, clear responsibility.
    
    Returns:
        Cached instance of application settings
    """
    return Settings()

# Create a global instance of settings
settings = get_settings()

# Simplified access to common settings
API_V1_STR = settings.API_V1_STR
PROJECT_NAME = settings.PROJECT_NAME
DEBUG = settings.DEBUG
ENVIRONMENT = settings.ENVIRONMENT
LOG_LEVEL = settings.LOG_LEVEL