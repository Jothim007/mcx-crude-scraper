from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

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
        
        # Verify access
        if "access denied" in driver.title.lower():
            raise Exception("Access denied detected")
            
        # Check if home page is loaded
        print("🏠 Home page title:", driver.title)
        print("✅ Successfully accessed MCX home page")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        driver.quit()
        print("🛑 Browser closed")

if __name__ == "__main__":
    main()
