from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
import time
import random
import re

def get_random_agent():
    desktop = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{}.0.{}.{} Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_{}_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{}.0.{}.{} Safari/537.36"
    ]
    version = (random.randint(100, 119), random.randint(1000, 9999), random.randint(100, 999)
    return random.choice(desktop).format(*version)

def human_type(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.3))

def setup_driver():
    chrome_options = Options()
    
    # Basic settings
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    # Advanced evasion
    chrome_options.add_argument(f"--user-agent={get_random_agent()}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    # Network settings
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    
    # Use system chromedriver
    service = Service(executable_path='/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Modify navigator properties
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
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

def bypass_cloudflare(driver):
    try:
        # Check if Cloudflare challenge exists
        if "challenge-form" in driver.page_source:
            print("🛡️ Cloudflare detected - attempting bypass...")
            time.sleep(5)
            driver.save_screenshot("cloudflare.png")
            return False
        return True
    except:
        return False

def main():
    print("🚀 Starting advanced browser session...")
    driver = setup_driver()
    
    try:
        print("🌐 Navigating to MCX with randomized patterns...")
        
        # Initial navigation with randomized delays
        driver.get("https://www.google.com")
        time.sleep(random.uniform(2, 4))
        driver.get("https://www.mcxindia.com")
        
        # Randomized scrolling
        for _ in range(random.randint(2, 4)):
            scroll_px = random.randint(300, 800)
            driver.execute_script(f"window.scrollBy(0, {scroll_px})")
            time.sleep(random.uniform(0.5, 1.5))
        
        # Check for blocking
        if not bypass_cloudflare(driver):
            raise Exception("Cloudflare blocking detected")
        
        print(f"📄 Final Title: {driver.title}")
        driver.save_screenshot("result.png")
        print("✅ Screenshot saved")
        
    except Exception as e:
        print(f"❌ Critical Error: {str(e)}")
        driver.save_screenshot("error.png")
    finally:
        driver.quit()
        print("🛑 Session terminated")

if __name__ == "__main__":
    main()
