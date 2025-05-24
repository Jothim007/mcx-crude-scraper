from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import random
import os

# Configuration
MOBILE_DEVICES = [
    {"deviceName": "iPhone 12"},
    {"deviceName": "Galaxy S21"},
    {"deviceName": "Pixel 5"}
]
DELAY_RANGE = (2, 5)  # Random delay range between actions (seconds)

def get_random_user_agent():
    mobile_agents = [
        # iPhone
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
        # Android
        "Mozilla/5.0 (Linux; Android 12; SM-S906N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36",
        # iPad
        "Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
    ]
    return random.choice(mobile_agents)

def human_interaction(driver):
    """Simulate human-like behavior"""
    actions = ActionChains(driver)
    
    # Random scrolling
    for _ in range(random.randint(2, 4)):
        scroll_amount = random.randint(200, 800)
        actions.scroll_by_amount(0, scroll_amount).perform()
        time.sleep(random.uniform(0.5, 1.5))
    
    # Random mouse movements
    actions.move_by_offset(
        random.randint(10, 50),
        random.randint(10, 50)
    ).perform()

def setup_driver():
    chrome_options = Options()
    
    # Mobile device emulation
    chrome_options.add_experimental_option(
        "mobileEmulation", random.choice(MOBILE_DEVICES)
    )
    
    # Stealth settings
    chrome_options.add_argument(f"--user-agent={get_random_user_agent()}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    # Network settings
    chrome_options.add_argument("--no-proxy-server")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument("--ignore-certificate-errors")
    
    # Headless mode with new Chrome headless
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=375,812")  # Mobile resolution
    
    # Use system Chromedriver
    driver = webdriver.Chrome(
        service=Service('/usr/bin/chromedriver'),
        options=chrome_options
    )
    
    # Remove navigator.webdriver flag
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    
    return driver

def access_website(driver, url):
    """Attempt to access website with human-like pattern"""
    try:
        # Initial access
        driver.get("https://www.google.com")
        time.sleep(random.uniform(*DELAY_RANGE))
        
        # Navigate to target
        driver.get(url)
        time.sleep(random.uniform(*DELAY_RANGE))
        
        # Human interaction
        human_interaction(driver)
        
        # Verify access
        if "access denied" in driver.title.lower():
            raise Exception("Access denied detected")
            
        return True
        
    except Exception as e:
        print(f"⚠️ Access attempt failed: {str(e)}")
        return False

def main():
    print("🚀 Starting mobile emulation browser...")
    driver = setup_driver()
    
    try:
        if access_website(driver, "https://www.mcxindia.com"):
            print("✅ Successfully accessed website")
            print(f"📱 Mobile View: {driver.title}")
            driver.save_screenshot("success.png")
        else:
            raise Exception("Failed after retries")
            
    except Exception as e:
        print(f"❌ Critical error: {str(e)}")
        driver.save_screenshot("error.png")
    finally:
        driver.quit()
        print("🛑 Session ended")

if __name__ == "__main__":
    main()
