from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    # Application configurations
    APP_NAME: str = "Document Management System"
    VERSION: str = "1.0.0"

    # Database settings
    DATABASE_URL: str

    # AWS S3 settings
    # AWS_ACCESS_KEY_ID: str
    # AWS_SECRET_ACCESS_KEY: str
    # S3_BUCKET_NAME: str

    # JWT settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    # Elasticsearch settings (if needed for query handling)
    ELASTICSEARCH_URL: str

    # Unstructured Keys
    UNSTRUCTURED_API_KEY: str
    UNSTRUCTURED_API_URL: str
    
    OPEN_AI_SECRET_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
