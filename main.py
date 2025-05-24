from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    return webdriver.Chrome(options=chrome_options)

def main():
    print("🌐 Launching browser...")
    driver = setup_driver()
    
    try:
        print("🔍 Opening MCX website...")
        driver.get("https://www.mcxindia.com")
        time.sleep(3)  # Wait for page to load
        
        # Debug output
        print("\n=== PAGE DEBUG INFO ===")
        print(f"Title: {driver.title}")
        print(f"URL: {driver.current_url}")
        print(f"Page source length: {len(driver.page_source)} characters")
        
        # Check for Cloudflare or other blockers
        if "cloudflare" in driver.page_source.lower():
            print("⚠️ Detected Cloudflare protection")
        
        # Save screenshot for debugging
        driver.save_screenshot("page.png")
        print("📸 Saved screenshot as page.png")
        
        # Basic verification
        if any(x in driver.title.lower() for x in ["mcx", "commodity", "exchange"]):
            print("✅ Successfully accessed MCX website")
        else:
            print("❌ Unexpected page content")
            
    except Exception as e:
        print(f"⚠️ Error occurred: {str(e)}")
    finally:
        driver.quit()
        print("🛑 Browser closed")

if __name__ == "__main__":
    main()
