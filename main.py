from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
import sys

def setup_driver():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        
        # Mimic human browser
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
        
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"🚨 Failed to setup driver: {str(e)}")
        sys.exit(1)

def main():
    print("=== MCX Website Debugger ===")
    print("🌐 Initializing browser...")
    
    driver = setup_driver()
    screenshot_path = "mcx_debug.png"
    
    try:
        # Step 1: Load page
        print("\n🔍 Navigating to MCX...")
        driver.get("https://www.mcxindia.com")
        time.sleep(5)  # Wait for page load

        # Step 2: Save visual proof
        driver.save_screenshot(screenshot_path)
        print(f"📸 Saved screenshot to: {screenshot_path}")

        # Step 3: Gather debug info
        print("\n=== PAGE ANALYSIS ===")
        print(f"Title: '{driver.title}'")
        print(f"Current URL: {driver.current_url}")
        print(f"Page source length: {len(driver.page_source)} chars")
        
        # Check for common blockers
        page_text = driver.page_source.lower()
        if "cloudflare" in page_text:
            print("🛡️ Cloudflare protection detected!")
        if "captcha" in page_text:
            print("🤖 CAPTCHA challenge detected!")
        if "access denied" in page_text:
            print("⛔ Access denied by website")

        # Verify MCX-specific content
        if any(x in driver.title.lower() for x in ["mcx", "commodity"]):
            print("✅ MCX website verified")
        else:
            print("❌ Unexpected page content")

    except Exception as e:
        print(f"\n⚠️ Critical error: {str(e)}")
        if 'driver' in locals():
            driver.save_screenshot("error.png")
            print("📸 Saved error screenshot")
    finally:
        driver.quit()
        print("\n🛑 Browser session ended")

if __name__ == "__main__":
    main()
