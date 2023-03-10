##########################################################################################################################

# Imports
import os, signal
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebElement

from urllib.parse import quote, urlencode, urlparse, urlunparse, parse_qs

##########################################################################################################################

# Sets options for Firefox Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_prefs = {}
chrome_options.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}

##########################################################################################################################

def scrape_url(driver: webdriver.Chrome, address: str):
    try:
        # Navigate driver
        driver.get('https://maps.google.com/maps?q=' + quote(address))
        
        # Search for element
        element: WebElement = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[jsaction="pane.heroHeaderImage.click"] >img')
            )
        )

        # Get source
        url = element.get_attribute('src')        

        # Return Data
        return True, url
    except Exception as error:
        return False, error

##########################################################################################################################

def fix_image_size(url: str):
    try:
        fixed_url = ''
        if 'googleusercontent' in url:
            split_url = url.split('=')
            if len(split_url) > 1: split_url.pop()
            fixed_url = '='.join(split_url)
        else:
            parsed_url = urlparse(url)
            query = parse_qs(parsed_url.query, keep_blank_values=True)
            query['w'] = ['999999']
            query['h'] = ['999999']
            parsed_url = parsed_url._replace(query=urlencode(query, True))
            fixed_url = urlunparse(parsed_url)

        # Return Data
        return True, fixed_url
    except Exception as error:
        return False, error

##########################################################################################################################

def url(address: str):
    res = scrape_url(address)
    ok, url = res
    if not ok: return res
    else: return fix_image_size(url)

##########################################################################################################################

def launch_driver():
    return webdriver.Chrome(options=chrome_options)

##########################################################################################################################

def kill_driver(driver: webdriver.Chrome):
    try:
        # Close driver
        driver.close()
        driver.quit()
        
        # Kill All Chrome Processes
        for line in os.popen("ps ax | grep chrome | grep -v grep"):
            fields = line.split()
            pid = fields[0]
            os.kill(int(pid), signal.SIGKILL)
            print("Killed Process " + pid + " in " + line)
        
        # Return Data
        return True
    except Exception as error:
        print(f"Error killing processes: {error}")
        return False

##########################################################################################################################
