from pydantic_settings import BaseSettings
from typing import Optional
from urllib.parse import urlparse
from pydantic import Field


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Database settings
    database_url: str = Field(..., alias="DATABASE_URL")

    # JWT settings
    better_auth_secret: str = "your-super-secret-jwt-key-for-development-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiry_days: int = 7
    access_token_expire_minutes: int = 30

    # Application settings
    env: str = "development"
    api_port: int = 8000

    # API settings
    api_v1_prefix: str = "/api/v1"
    debug: bool = True
    project_name: str = "Todo API"
    version: str = "1.0.0"
    api_docs_enabled: bool = True

    # CORS settings
    backend_cors_origins: str = "*"  # In production, restrict this to specific origins

    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "ignore"  # This allows extra environment variables to be ignored
    }


def get_settings() -> Settings:
    """
    Get application settings instance.
    """
    return Settings()


# Create a global settings instance
settings = Settings()


def is_valid_database_url(url: str) -> bool:
    """
    Validate that a database URL is properly formatted for PostgreSQL.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc]) and result.scheme in ['postgresql', 'postgres']
    except Exception:
        return False


# Validate settings on import
if not is_valid_database_url(settings.database_url):
    raise ValueError(f"Invalid DATABASE_URL: {settings.database_url}")

# Validate that critical secrets are not using default values in production
if settings.env == "production":
    if settings.better_auth_secret == "your-super-secret-jwt-key-for-development-change-in-production":
        raise ValueError("BETTER_AUTH_SECRET must be set to a secure value in production")