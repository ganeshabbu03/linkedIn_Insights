from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from app.models.page import Page
from app.services.scraper import LinkedInScraper
from beanie.operators import RegEx, GTE, LTE

router = APIRouter()
scraper = LinkedInScraper()

from aiocache import cached, Cache

@router.get("/page/{page_id}", response_model=Page)
@cached(ttl=300, key_builder=lambda f, *args, **kwargs: f"page_{kwargs['page_id']}")
async def get_page_details(page_id: str):
    # Check DB
    page = await Page.find_one(Page.id == page_id)
    if page:
        return page
    
    # Scrape
    scraped_data = await scraper.scrape_page(page_id)
    if scraped_data:
        # Save to DB
        await scraped_data.save()
        return scraped_data
    
    raise HTTPException(status_code=404, detail="Page not found and could not be scraped")

@router.get("/pages", response_model=List[Page])
async def list_pages(
    min_followers: Optional[int] = None,
    max_followers: Optional[int] = None,
    industry: Optional[str] = None,
    name: Optional[str] = None,
    limit: int = 10,
    skip: int = 0
):
    query = Page.find_all()
    
    if min_followers is not None:
        query = query.find(Page.followers_count >= min_followers)
    if max_followers is not None:
        query = query.find(Page.followers_count <= max_followers)
    if industry:
        # Case insensitive regex match
        query = query.find(RegEx(Page.industry, industry, "i"))
    if name:
        query = query.find(RegEx(Page.name, name, "i"))
        
    return await query.limit(limit).skip(skip).to_list()

from app.services.ai_service import AIService
ai_service = AIService()

@router.get("/page/{page_id}/summary")
async def get_page_summary(page_id: str):
    page = await Page.find_one(Page.id == page_id)
    if not page:
        # Try finding fetch first? Or assume user calls details first?
        # Let's try fetch if not exists
        page = await scraper.scrape_page(page_id)
        if not page:
           raise HTTPException(status_code=404, detail="Page not found")
        await page.save()
        
    summary = await ai_service.generate_summary(page)
    return {"page_id": page_id, "summary": summary}
