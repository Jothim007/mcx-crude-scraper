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

def check_homepage_access(driver):
    print("🌐 Attempting to access MCX homepage...")
    driver.get("https://www.mcxindia.com")
    time.sleep(3)  # Wait for page to load
    
    # Check page title and URL
    print(f"📄 Page Title: {driver.title}")
    print(f"🌍 Current URL: {driver.current_url}")
    
    # Verify successful access
    if "MCX India" in driver.title:
        print("✅ Successfully accessed MCX homepage")
        return True
    elif "access denied" in driver.title.lower():
        print("⛔ Access denied by website")
        return False
    else:
        print("⚠️ Unexpected page content")
        return False

def main():
    driver = setup_driver()
    try:
        if check_homepage_access(driver):
            # If accessed successfully, you can add more checks here
            print("🔄 Checking for homepage elements...")
            # Example: Check if the option chain link exists
            try:
                option_chain_link = driver.find_element("link text", "Option Chain")
                print("🔗 Found Option Chain link")
            except:
                print("❌ Option Chain link not found")
        else:
            print("❌ Failed to access MCX homepage")
            
    except Exception as e:
        print(f"💥 Unexpected error: {str(e)}")
    finally:
        driver.quit()
        print("🛑 Browser session closed")

if __name__ == "__main__":
    main()
