import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = uc.Chrome(options=options)
driver.get("https://www.mcxindia.com")

time.sleep(5)  # Give it time to load
print("MCX website opened")

# Save screenshot
driver.save_screenshot("mcx_screenshot.png")
driver.quit()

