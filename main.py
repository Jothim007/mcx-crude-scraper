from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    return driver

def main():
    print("🌐 Launching browser...")
    driver = setup_driver()
    
    try:
        print("🔍 Opening MCX website...")
        driver.get("https://www.mcxindia.com")
        
        # Verify page loaded
        if "MCX India" in driver.title:
            print("✅ Successfully opened MCX website")
            print(f"📄 Page title: {driver.title}")
        else:
            print("❌ Failed to load MCX website")
            
    except Exception as e:
        print(f"⚠️ Error occurred: {str(e)}")
    finally:
        driver.quit()
        print("🛑 Browser closed")

if __name__ == "__main__":
    main()
