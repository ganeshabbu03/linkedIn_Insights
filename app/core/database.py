from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import get_settings
from app.models.page import Page
from app.models.post import Post

import certifi

async def init_db():
    settings = get_settings()
    
    # Only use SSL/TLS certificates for Atlas (srv) connections
    if "mongodb+srv" in settings.MONGO_URL:
        client = AsyncIOMotorClient(settings.MONGO_URL, tlsCAFile=certifi.where())
    else:
        # Local connection (usually no SSL)
        client = AsyncIOMotorClient(settings.MONGO_URL)
        
    await init_beanie(database=client[settings.DATABASE_NAME], document_models=[Page, Post])
