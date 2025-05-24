from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=chrome_options)

def main():
    print("🌐 Launching browser...")
    driver = setup_driver()
    
    try:
        print("🔍 Opening MCX website...")
        driver.get("https://www.mcxindia.com")
        time.sleep(5)  # Wait longer for page load
        
        # Save screenshot (will be saved in the workflow's workspace)
        screenshot_path = "mcx_screenshot.png"
        driver.save_screenshot(screenshot_path)
        print(f"📸 Saved screenshot to: {os.path.abspath(screenshot_path)}")
        
        # Debug output
        print(f"\n=== PAGE DEBUG ===")
        print(f"Title: {driver.title}")
        print(f"URL: {driver.current_url}")
        print(f"Page contains 'MCX': {'MCX' in driver.page_source}")
        
    except Exception as e:
        print(f"⚠️ Error: {str(e)}")
        if 'driver' in locals():
            driver.save_screenshot("error.png")
            print("📸 Saved error screenshot")
    finally:
        driver.quit()
        print("🛑 Browser closed")

if __name__ == "__main__":
    main()
