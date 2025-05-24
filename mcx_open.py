from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
driver.get("https://www.mcxindia.com")
time.sleep(5)

driver.save_screenshot("mcx_screenshot.png")
print("Screenshot saved")

driver.quit()
