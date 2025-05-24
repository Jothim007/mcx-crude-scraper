from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import random
import time

# 1. Proxy Configuration (Rotate multiple proxies)
PROXIES = [
    "http://user:pass@proxy1:port",  # Replace with real proxies
    "http://user:pass@proxy2:port",
    "http://user:pass@proxy3:port"
]

# 2. Advanced Anti-Detection
def setup_driver():
    chrome_options = Options()
    
    # Proxy Setup
    proxy = random.choice(PROXIES)
    chrome_options.add_argument(f"--proxy-server={proxy}")
    
    # Stealth Settings
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    # Network Spoofing
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--ignore-certificate-errors")
    
    # Use system Chromedriver
    driver = webdriver.Chrome(
        service=Service('/usr/bin/chromedriver'),
        options=chrome_options
    )
    
    # Override WebDriver flag
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

# Usage
driver = setup_driver()
try:
    driver.get("https://www.mcxindia.com")
    time.sleep(5)
    driver.save_screenshot("result.png")
finally:
    driver.quit()
