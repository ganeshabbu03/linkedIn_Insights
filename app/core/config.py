from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "LinkedIn Insights"
    MONGO_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "linkedin_insights"
    HUGGINGFACE_API_KEY: str = "" # User must provide this in .env
    LINKEDIN_COOKIE: str | None = None
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=False
    )

@lru_cache()
def get_settings():
    return Settings()
