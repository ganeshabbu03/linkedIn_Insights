from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "LinkedIn Insights"
    MONGO_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "linkedin_insights"
    HUGGINGFACE_API_KEY: str = "" # User must provide this in .env
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
