import sys
import asyncio
import uvicorn

# 1. SETUP: Force Windows to use the correct Event Loop (Proactor)

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())



from app.api import app

if __name__ == "__main__":
    print("🚀 Starting FinScout Automation Engine (Production Mode)...")
    
    # 3. RUN: Disable 'reload' to prevent spawning child processes that break the loop
    # We pass the 'app' object directly, not the string "app.api:app"
    uvicorn.run(app, host="0.0.0.0", port=8000)