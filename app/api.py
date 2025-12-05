from fastapi import FastAPI, HTTPException, BackgroundTasks
from app.scraper import MarketScraper
from app.etl import DataTransformer
from app.database import db

app = FastAPI(title="FinScout Automation API")

# Helper function to run the full pipeline
async def run_pipeline_task():
    scraper = MarketScraper()
    raw_data = await scraper.fetch_data()
    if raw_data:
        clean_data = DataTransformer.clean(raw_data)
        db.save_bulk(clean_data)

@app.get("/")
def home():
    return {"message": "Welcome to FinScout. Use /trigger to start scraping."}

@app.post("/trigger")
async def trigger_automation(background_tasks: BackgroundTasks):
    """
    Endpoint to manually trigger the scraping bot.
    Runs in the background so the API doesn't freeze.
    """
    background_tasks.add_task(run_pipeline_task)
    return {"status": "Pipeline started in background"}

@app.get("/data")
def get_data():
    """Fetch all scraped data from the database."""
    return db.get_all()