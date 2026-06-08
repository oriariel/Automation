import setuptools  
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_setup():
    print("🚀 Launching anti-detect Chrome browser...")
    
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options, version_main=148)
    
    try:
        print("🌐 Navigating to Wikipedia...")
        driver.get("https://www.wikipedia.org/")
        
        # ⏳ EXPLICIT WAIT: Wait up to 10 seconds for the basic page structure to exist
        print("⏳ Waiting for page body to load...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Foolproof check: Get the page title directly from the browser metadata
        page_title = driver.title
        print(f"✅ Success! Connected to the browser. Page Title is: '{page_title}'")
        
    except Exception as e:
        print(f"❌ Something went wrong: {e}")
        
    finally:
        print("🔒 Attempting to close browser...")
        try:
            driver.quit()
        except OSError:
            pass
        print("✨ Done!")

if __name__ == "__main__":
    test_setup()