import asyncio
from playwright.async_api import async_playwright
import logging
import os

logger = logging.getLogger(__name__)

class MarketScraper:
    # URL for most active stocks
    BASE_URL = "https://finance.yahoo.com/most-active"

    async def fetch_data(self):
        logger.info("Launching Playwright...")
        data = []

        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
            
            # Create a context with a real User Agent
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            
            # Block heavy resources (Images, Fonts, CSS) to speed up loading by 5x
            await context.route("**/*.{png,jpg,jpeg,svg,css,woff,woff2}", lambda route: route.abort())
            
            page = await context.new_page()
            
            try:
                logger.info(f"Navigating to {self.BASE_URL}")
                
                # --- CRITICAL FIX ---
                # wait_until="domcontentloaded": Stops waiting once HTML is ready (ignores spinning ads)
                # timeout=60000: Gives it 60 seconds
                await page.goto(self.BASE_URL, timeout=60000, wait_until="domcontentloaded")
                
                # Wait for the specific table to appear
                await page.wait_for_selector('table tbody tr', timeout=15000)

                # Grab all rows
                rows = await page.locator('table tbody tr').all()
                
                # Iterate through the first 10 rows
                for row in rows[:10]:
                    cells = await row.locator('td').all_inner_texts()
                    # Yahoo table structure check
                    if len(cells) > 5:
                        data.append({
                            "symbol": cells[0],
                            "name": cells[1],
                            "price_raw": cells[2], 
                            "change": cells[3],
                            "volume_raw": cells[5] 
                        })
                
                logger.info(f"Scraped {len(data)} raw records.")
                
            except Exception as e:
                logger.error(f"Error during scraping: {e}")
                # Try to take a screenshot
                try:
                    cwd = os.getcwd()
                    path = os.path.join(cwd, "error_screenshot.png")
                    await page.screenshot(path=path, timeout=5000)
                    logger.info(f"Screenshot saved to: {path}")
                except Exception as shot_error:
                    logger.error(f"Could not take screenshot: {shot_error}")
            finally:
                await browser.close()
        
        return data