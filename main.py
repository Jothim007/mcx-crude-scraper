from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
import time
import random

def get_random_agent():
    desktop = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{0}.0.{1}.{2} Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_{3}_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{0}.0.{1}.{2} Safari/537.36"
    ]
    version = (
        random.randint(100, 119),  # Chrome major version
        random.randint(1000, 9999),  # Build number
        random.randint(100, 999),   # Patch number
        random.randint(12, 15)      # macOS version
    )
    return random.choice(desktop).format(*version)

def setup_driver():
    chrome_options = Options()
    
    # Basic settings
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Advanced evasion
    chrome_options.add_argument(f"--user-agent={get_random_agent()}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    # Use system chromedriver
    service = Service(executable_path='/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Apply stealth
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
    print("🚀 Starting browser session...")
    driver = setup_driver()
    
    try:
        print("🌐 Navigating to MCX...")
        driver.get("https://www.mcxindia.com")
        time.sleep(5)
        
        print(f"📄 Page Title: {driver.title}")
        print(f"🌍 Current URL: {driver.current_url}")
        
        driver.save_screenshot("result.png")
        print("✅ Screenshot saved")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        driver.save_screenshot("error.png")
    finally:
        driver.quit()
        print("🛑 Session ended")

if __name__ == "__main__":
    main()
