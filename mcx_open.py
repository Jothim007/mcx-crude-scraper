from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os
from datetime import datetime

def capture_mcx_screenshot(url="https://www.mcxindia.com", save_dir="screenshots"):
    os.makedirs(save_dir, exist_ok=True)
    
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # For headless operation on server:
    chrome_options.add_argument("--headless=new")
    
    try:
        # Use system Chrome/Chromium
        driver = webdriver.Chrome(
            service=Service('/usr/bin/chromedriver'),
            options=chrome_options
        )
        
        driver.get(url)
        print(f"Opened: {url}")
        time.sleep(5)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(save_dir, f"mcx_screenshot_{timestamp}.png")
        driver.save_screenshot(filename)
        print(f"Screenshot saved to: {filename}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    capture_mcx_screenshot()
