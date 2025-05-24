from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time

# Setup screenshot directory
os.makedirs("screenshots", exist_ok=True)

def setup_driver():
    chrome_options = Options()
    
    # Headless with GPU (fixes blank screenshots)
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--force-device-scale-factor=1")  # Fixes scaling
    
    # Enable GPU for rendering
    chrome_options.add_argument("--use-gl=egl")
    chrome_options.add_argument("--disable-software-rasterizer")
    
    driver = webdriver.Chrome(
        service=Service('/usr/bin/chromedriver'),
        options=chrome_options
    )
    return driver

def wait_for_visible_element(driver, timeout=10):
    """Wait until page has visible content"""
    WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.XPATH, "//*[not(contains(@style,'display:none'))]"))
    )

def capture_screenshot(driver, filename):
    """Guaranteed screenshot capture"""
    try:
        # Scroll to trigger rendering
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3)")
        time.sleep(1)
        
        # Wait for visible content
        wait_for_visible_element(driver)
        
        # Double-check rendering
        if not driver.find_elements(By.XPATH, "//body/*"):
            raise Exception("No visible elements found")
            
        driver.save_screenshot(f"screenshots/{filename}")
        print(f"✅ Saved {filename}")
    except Exception as e:
        print(f"⚠️ Screenshot failed: {str(e)}")
        # Fallback screenshot
        driver.save_screenshot(f"screenshots/fallback_{filename}")

def main():
    driver = setup_driver()
    try:
        print("🌐 Loading MCX website...")
        driver.get("https://www.mcxindia.com")
        
        # Wait for page to stabilize
        time.sleep(3)
        
        # First screenshot attempt
        capture_screenshot(driver, "page.png")
        
        # Additional verification
        if "access denied" in driver.title.lower():
            raise Exception("Access denied")
            
        print(f"🖥️ Page title: {driver.title}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        capture_screenshot(driver, "error.png")
    finally:
        driver.quit()
        print("🛑 Session ended")

if __name__ == "__main__":
    main()
