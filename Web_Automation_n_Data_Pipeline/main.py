# main.py
import os
import setuptools  
import undetected_chromedriver as uc
from config.config import CHROME_VERSION, TARGET_URL
from pages.search_page import SearchPage
from utils.db_manager import DatabaseManager  # 👈 Import the DB layer

# Monkey patch the buggy library destructor to prevent WinError 6 on script exit
_orig_del = uc.Chrome.__del__
def _safe_del(self):
    try:
        _orig_del(self)
    except OSError:
        pass
uc.Chrome.__del__ = _safe_del


def run_pipeline():
    print("🤖 Initializing SentinelScrape Automation Engine...")
    
    # Ensure the data directory exists for the SQLite file
    os.makedirs("data", exist_ok=True)
    
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options, version_main=CHROME_VERSION)
    
    try:
        # Initialize our page objects and database components
        scraper = SearchPage(driver)
        db = DatabaseManager()  # 👈 Initialize database
        
        print(f"🌐 Navigating to production target... ")
        scraper.navigate_to(TARGET_URL)
        
        print("⚡ Executing dynamic DOM extraction...")
        scraped_items = scraper.extract_product_data()
        
        print(f"\n📊 Extraction Complete! Found {len(scraped_items)} data entries.")
        
        # 💾 Pipe data directly into the database engine
        db.save_products(scraped_items)
        
    except Exception as e:
        print(f"💥 Pipeline Execution Failed: {e}")
        
    finally:
        print("🔒 Safely tearing down automation processes...")
        try:
            driver.quit()
        except OSError:
            pass
        print("✨ Process Execution Finished.")

if __name__ == "__main__":
    run_pipeline()