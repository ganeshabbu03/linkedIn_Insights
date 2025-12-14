from fastapi import FastAPI
from contextlib import asynccontextmanager
import sys
import asyncio

# Fix for Windows asyncio loop with Playwright (Needs to be in main.py for Uvicorn reload workers)
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from app.core.database import init_db
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(title="LinkedIn Insights API", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def root():
    return FileResponse("app/static/index.html")

from app.api.routes import router as api_router
app.include_router(api_router, prefix="/api/v1")
