from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os
from datetime import datetime
import math

def round_to_nearest_100(val):
    val = int(float(val))
    lower = (val // 100) * 100
    upper = lower + 100
    return lower, upper

def get_next_available_row(sheet):
    str_list = list(filter(None, sheet.col_values(2)))  # Column B
    return len(str_list) + 1

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--remote-debugging-port=9222")
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    return driver

def main():
    # Load environment variables
    GS_CREDENTIALS = json.loads(os.getenv('GS_CREDENTIALS'))
    SHEET_ID = os.getenv('SHEET_ID')
    
    # Initialize driver
    driver = setup_driver()
    
    try:
        # === Step 1: Scrape MCX Option Chain ===
        driver.get("https://www.mcxindia.com/market-data/option-chain")
        wait = WebDriverWait(driver, 20)

        wait.until(EC.element_to_be_clickable((By.ID, "ctl00_cph_InnerContainerRight_C008_ddlSymbols_Arrow"))).click()
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//li[text()='CRUDEOIL']"))).click()
        print("✅ Selected commodity: CRUDEOIL")

        expiry_dropdown = wait.until(EC.presence_of_element_located((By.ID, "ddlExpiry")))
        expiry_select = Select(expiry_dropdown)
        expiry_text = "16JUN2025"

        try:
            expiry_select.select_by_visible_text(expiry_text)
            print(f"✅ Selected expiry: {expiry_text}")
        except:
            print(f"❌ Expiry '{expiry_text}' not found.")
            driver.quit()
            return

        show_button = wait.until(EC.element_to_be_clickable((By.ID, "btnShow")))
        show_button.click()
        print("✅ Clicked Show button")
        time.sleep(3)

        underlying_elem = wait.until(EC.presence_of_element_located((By.ID, "UValue")))
        underlying_value = underlying_elem.text.strip()
        print(f"✅ Underlying value: {underlying_value}")

        table = wait.until(EC.presence_of_element_located((By.ID, "tblOptionChain")))

        headers = [
            "",  # Matches site format
            "CALL_OI (Lots)", "CALL_Chng in OI", "CALL_Volume", "CALL_LTP", "CALL_Abs. Chng",
            "CALL_Bid Qty", "CALL_Bid Price", "CALL_Ask Price", "CALL_Ask Qty",
            "Strike Price",
            "PUT_Bid Qty", "PUT_Bid Price", "PUT_Ask Price", "PUT_Ask Qty",
            "PUT_Abs. Chng", "PUT_LTP", "PUT_Volume", "PUT_Chng in OI", "PUT_OI (Lots)"
        ]

        expected_columns = 20
        cleaned_rows = []

        for row in table.find_elements(By.XPATH, ".//tbody/tr"):
            cells = row.find_elements(By.TAG_NAME, "td")
            row_data = [cell.text.strip() for cell in cells]

            if not any(row_data):
                continue

            if len(row_data) < expected_columns:
                row_data.extend([''] * (expected_columns - len(row_data)))
            elif len(row_data) > expected_columns:
                row_data = row_data[:expected_columns]

            cleaned_rows.append(row_data)

        print(f"✅ Extracted {len(cleaned_rows)} rows.")

        # === Step 2: Upload to Google Sheets ===
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(GS_CREDENTIALS, scope)
        client = gspread.authorize(creds)

        sheet1 = client.open_by_key(SHEET_ID).worksheet("Sheet1")
        sheet2 = client.open_by_key(SHEET_ID).worksheet("Sheet2")
        sheet3 = client.open_by_key(SHEET_ID).worksheet("Sheet3")

        # Clear and write Sheet1
        sheet1.clear()
        group_row = [''] + ['CALLS'] * 9 + [''] + ['PUTS'] * 9
        data_to_write = [group_row, headers] + cleaned_rows
        sheet1.update('A1', data_to_write)
        sheet1.update('U3', [["Underlying Value"]])
        sheet1.update('U4', [[underlying_value]])

        # Basic formatting
        sheet1.freeze(rows=1)
        sheet1.merge_cells('B1:J1')
        sheet1.merge_cells('L1:T1')
        
        # === Step 3: Filter and Append to Sheet2 & Sheet3 ===
        lower_strike, upper_strike = round_to_nearest_100(underlying_value)

        strike_index = headers.index("Strike Price")
        matching_lower = next((row for row in cleaned_rows if row[strike_index] == str(lower_strike)), None)
        matching_upper = next((row for row in cleaned_rows if row[strike_index] == str(upper_strike)), None)

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if matching_lower:
            row_num = get_next_available_row(sheet2)
            sheet2.update('A1', [[str(lower_strike)]])
            sheet2.update(f'A{row_num}', [[timestamp] + matching_lower])

        if matching_upper:
            row_num = get_next_available_row(sheet3)
            sheet3.update('A1', [[str(upper_strike)]])
            sheet3.update(f'A{row_num}', [[timestamp] + matching_upper])

        print(f"✅ Data for strikes {lower_strike} → Sheet2, {upper_strike} → Sheet3")

    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        raise
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
