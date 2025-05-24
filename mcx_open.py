import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time

def get_driver():
    options = uc.ChromeOptions()
    
    # Stealth settings
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--ignore-certificate-errors")
    
    # Randomize user agent
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    ]
    options.add_argument(f'--user-agent={random.choice(user_agents)}')
    
    # Headless mode (disable if testing)
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    
    # Disable automation flags
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    driver = uc.Chrome(options=options, use_subprocess=True)
    
    # Remove navigator.webdriver flag
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

try:
    print("Launching stealth browser...")
    driver = get_driver()
    
    print("Accessing MCX website...")
    driver.get("https://www.mcxindia.com")
    
    # Random delay to mimic human behavior
    time.sleep(random.uniform(2, 5))
    
    # Wait for page to load
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    
    print("Taking screenshot...")
    driver.save_screenshot("mcx_screenshot.png")
    print("✅ Screenshot saved successfully!")

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    if 'driver' in locals():
        driver.quit()
    print("Browser closed.")
