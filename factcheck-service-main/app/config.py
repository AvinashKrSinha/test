# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Existing GCP and Vertex AI settings
    project_id: str
    region: str
    gemini_model: str
    gcs_bucket: str
    whatsapp_token: str
    telegram_token: str
    index_endpoint_id: str
    
    # New settings for MongoDB and JWT Auth
    mongo_details: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # Pydantic v2 configuration
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()