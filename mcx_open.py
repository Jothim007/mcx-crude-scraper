from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

# 1. Use premium proxies (not free/public ones)
PROXIES = [
    "http://username:password@geo.iproyal.com:12321",  # Example paid proxy
    "http://customer-USERNAME-cc-US:SESSIONID@zproxy.lum-superproxy.io:22225"
]

def setup_driver():
    chrome_options = Options()
    
    # Select proxy
    proxy = PROXIES[0]  # Rotate these in production
    
    # Configure proxy properly
    chrome_options.add_argument(f"--proxy-server={proxy}")
    chrome_options.add_argument("--ignore-certificate-errors")
    
    # Essential settings
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Authentication for proxy (if required)
    plugin = """
    var config = {
        mode: "fixed_servers",
        rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: %d
            },
            bypassList: ["localhost"]
        }
    };
    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    """ % (proxy.split('@')[-1].split(':')[0], int(proxy.split(':')[-1]))
    
    chrome_options.add_extension(create_proxy_extension(plugin))
    
    driver = webdriver.Chrome(
        service=Service('/usr/bin/chromedriver'),
        options=chrome_options
    )
    return driver

def create_proxy_extension(proxy_config):
    from selenium.webdriver.common.utils import free_port
    import zipfile
    import os
    
    ext_dir = "/tmp/proxy_ext"
    os.makedirs(ext_dir, exist_ok=True)
    
    with open(f"{ext_dir}/manifest.json", "w") as f:
        f.write("""
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": ["proxy", "tabs", "unlimitedStorage", "storage"],
            "background": {"scripts": ["background.js"]},
            "minimum_chrome_version": "76.0.0"
        }
        """)
    
    with open(f"{ext_dir}/background.js", "w") as f:
        f.write(proxy_config)
    
    proxy_ext = f"{ext_dir}.zip"
    with zipfile.ZipFile(proxy_ext, 'w') as zp:
        zp.write(f"{ext_dir}/manifest.json", "manifest.json")
        zp.write(f"{ext_dir}/background.js", "background.js")
    
    return proxy_ext

# Usage
driver = setup_driver()
try:
    driver.get("https://www.mcxindia.com")
    print("Success:", driver.title)
    driver.save_screenshot("mcx_screenshot.png")
except Exception as e:
    print("Failed:", str(e))
    driver.save_screenshot("error.png")
finally:
    driver.quit()
