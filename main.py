from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Set up headless Chrome
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Start the browser
driver = webdriver.Chrome(options=options)

# Open MCX website
driver.get("https://www.mcxindia.com")

# Wait for page to load
time.sleep(5)

# Save screenshot
driver.save_screenshot("mcx_homepage.png")

# Quit the browser
driver.quit()
