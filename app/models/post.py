from beanie import Document
from typing import Optional
from datetime import datetime

class Post(Document):
    post_id: str # LinkedIn unique post identifier
    page_id: str # References Page.id
    content: Optional[str] = None
    likes_count: int = 0
    comments_count: int = 0
    share_count: int = 0
    media_url: Optional[str] = None
    post_url: Optional[str] = None
    
    posted_at: Optional[str] = None # Or datetime if parsed
    created_at: datetime = datetime.now()

    class Settings:
        name = "posts"
