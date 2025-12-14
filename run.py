import asyncio
import sys
import uvicorn

if __name__ == "__main__":
    # Windows specific event loop policy to allow subprocesses (required for Playwright)
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
