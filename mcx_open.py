import undetected_chromedriver as uc
import time

options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--headless=new")

driver = uc.Chrome(options=options, use_subprocess=True)
driver.get("https://www.mcxindia.com")
time.sleep(5)

driver.save_screenshot("mcx_screenshot.png")
print("Screenshot saved")

driver.quit()
