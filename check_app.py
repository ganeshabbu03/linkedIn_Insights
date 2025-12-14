import asyncio
import os
try:
    from app.main import app
    from app.core.config import get_settings
    print("SUCCESS: App imports working.")
    print(f"Project: {get_settings().PROJECT_NAME}")
except Exception as e:
    print(f"ERROR: {e}")
