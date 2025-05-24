from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
import time
import os

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Anti-detection settings
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    # Use system ChromeDriver that comes with GitHub Actions
    driver = webdriver.Chrome(
        service=Service(executable_path='/usr/bin/chromedriver'),
        options=chrome_options
    )
    
    # Stealth configuration
    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    return driver

def main():
    print("🚀 Starting MCX Access...")
    driver = setup_driver()
    try:
        print("🌐 Navigating to MCX...")
        driver.get("https://www.mcxindia.com")
        time.sleep(5)
        
        print(f"📄 Page Title: {driver.title}")
        print(f"🌍 Current URL: {driver.current_url}")
        
        driver.save_screenshot("result.png")
        print("📸 Saved screenshot: result.png")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        if 'driver' in locals():
            driver.save_screenshot("error.png")
    finally:
        if 'driver' in locals():
            driver.quit()
        print("🛑 Browser closed")

if __name__ == "__main__":
    main()
