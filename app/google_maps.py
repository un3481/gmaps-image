
##########################################################################################################################

# Imports
from re import sub
from urllib.parse import quote, urlencode, urlparse, urlunparse, parse_qs

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebElement

##########################################################################################################################

# Sets options for Firefox Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_prefs = {}
chrome_options.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}

# Regular expresion for resizing usercontent images
usrctt_re = r'=w(\d+)-h(\d+)'

##########################################################################################################################

def url(address: str):
    try:
        # Launch driver
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://maps.google.com/maps?q=' + quote(address))
        
        # Search for element
        element: WebElement = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[jsaction="pane.heroHeaderImage.click"] >img')
            )
        )
        
        # Get source
        raw_image_url = element.get_attribute('src')
        
        # Close driver
        driver.close()
        
        # # Change image width and height
        # image_url = ''
        # if 'googleusercontent' in raw_image_url:
        #     resized = f'=w{width}-h{height}'
        #     image_url = sub(usrctt_re, resized, raw_image_url)
        # else:
        #     parsed_url = urlparse(raw_image_url)
        #     query = parse_qs(parsed_url.query, keep_blank_values=True)
        #     query['w'] = [f'{width}']
        #     query['h'] = [f'{height}']
        #     parsed_url = parsed_url._replace(query=urlencode(query, True))
        #     image_url = urlunparse(parsed_url)
        
        # Return Data
        return (True, raw_image_url)
    except Exception as error:
        return (False, error)

##########################################################################################################################
