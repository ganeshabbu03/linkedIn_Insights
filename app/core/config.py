from pydantic_settings import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "LinkedIn Insights"
    MONGO_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "linkedin_insights"
    HUGGINGFACE_API_KEY: str = "" # User must provide this in .env
    LINKEDIN_COOKIE: str | None = None
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
