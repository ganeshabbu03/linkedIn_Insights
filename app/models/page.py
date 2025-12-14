from beanie import Document
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class Employee(BaseModel):
    name: str
    profile_url: Optional[str] = None
    designation: Optional[str] = None

class Comment(BaseModel):
    author: str
    text: str
    likes: int = 0

class PagePost(BaseModel):
    # Embedded post for the Page document (optional, or store as separate collection)
    # The requirement says "Posts of the Page... stored... Relationships maintained"
    # We can store a summary here or reference the Post collection.
    # For MongoDB, embedding a few (15-25) is efficient.
    content: str
    likes: int = 0
    comments: List[Comment] = []
    post_url: Optional[str] = None
    posted_at: Optional[str] = None

class Page(Document):
    id: str # LinkedIn unique identifier (URL slug)
    name: str
    url: str
    description: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    followers_count: int = 0
    head_count: Optional[str] = None # e.g. "11-50 employees"
    location: Optional[str] = None
    profile_pic_url: Optional[str] = None
    specialities: Optional[List[str]] = []
    
    # Relationships/Embedded
    employees: List[Employee] = []
    recent_posts: List[PagePost] = [] # Storing top 15-25 here for easy access
    
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Settings:
        name = "pages"
