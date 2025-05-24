from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
import time

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Anti-detection settings
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    driver = webdriver.Chrome(options=chrome_options)
    
    # Apply stealth settings
    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    return driver

def main():
    driver = setup_driver()
    try:
        driver.get("https://www.mcxindia.com")
        time.sleep(5)
        print(f"Title: {driver.title}")
        driver.save_screenshot("result.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
