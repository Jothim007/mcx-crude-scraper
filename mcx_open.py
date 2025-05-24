"""
MCX Website Screenshot Tool
Author: [Your Name]
Description: Opens MCX website and captures screenshot with proper browser emulation
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from datetime import datetime

def capture_mcx_screenshot(url="https://www.mcxindia.com", save_dir="screenshots"):
    """
    Capture screenshot of MCX website
    
    Args:
        url (str): URL to capture (default: MCX homepage)
        save_dir (str): Directory to save screenshots
    """
    # Create directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)
    
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Add stealth options to avoid detection
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    try:
        # Initialize WebDriver
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        # Modify navigator.webdriver flag to prevent detection
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Open the URL
        driver.get(url)
        print(f"Opened: {url}")
        
        # Wait for page to load
        time.sleep(5)  # Adjust based on your internet speed
        
        # Generate timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(save_dir, f"mcx_screenshot_{timestamp}.png")
        
        # Capture screenshot
        driver.save_screenshot(filename)
        print(f"Screenshot saved to: {filename}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        # Close the browser
        if 'driver' in locals():
            driver.quit()
            print("Browser closed.")

if __name__ == "__main__":
    # Example usage
    capture_mcx_screenshot()
