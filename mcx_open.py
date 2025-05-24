from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    return driver

def main():
    os.makedirs("artifacts", exist_ok=True)
    driver = setup_driver()
    
    try:
        print("🌐 Navigating to MCX...")
        driver.get("https://www.mcxindia.com")
        time.sleep(5)  # Increased wait time
        
        screenshot_path = "artifacts/mcx-status.png"
        driver.save_screenshot(screenshot_path)
        print(f"📸 Saved verification screenshot to {screenshot_path}")
        
        if "access denied" in driver.title.lower():
            raise Exception("Access denied detected")
            
        print(f"✅ Success - Page Title: {driver.title}")
        
    except Exception as e:
        print(f"❌ Monitoring failed: {str(e)}")
        if 'driver' in locals():
            driver.save_screenshot("artifacts/mcx-error.png")
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    main()
