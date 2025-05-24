from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Set up headless Chrome
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Start browser
driver = webdriver.Chrome(options=options)

# Open MCX website
driver.get("https://www.mcxindia.com")
time.sleep(5)

# Take screenshot
screenshot_path = "mcx_screenshot.png"
driver.save_screenshot(screenshot_path)
print(f"Screenshot saved to {screenshot_path}")

driver.quit()
