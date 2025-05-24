from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
import time

# Ensure screenshots directory exists
os.makedirs("screenshots", exist_ok=True)

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Use system chromedriver
    driver = webdriver.Chrome(
        service=Service('/usr/bin/chromedriver'),
        options=chrome_options
    )
    return driver

def main():
    driver = setup_driver()
    try:
        print("🌐 Navigating to MCX...")
        driver.get("https://www.mcxindia.com")
        time.sleep(3)
        
        # Always save screenshot
        screenshot_path = "screenshots/result.png"
        driver.save_screenshot(screenshot_path)
        print(f"📸 Screenshot saved to {screenshot_path}")
        
        # Verify access
        if "access denied" in driver.title.lower():
            raise Exception("Access denied detected")
            
        print("✅ Successfully accessed MCX")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        error_path = "screenshots/error.png"
        driver.save_screenshot(error_path)
        print(f"📸 Error screenshot saved to {error_path}")
    finally:
        driver.quit()
        print("🛑 Browser closed")

if __name__ == "__main__":
    main()
