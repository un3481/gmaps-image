
##########################################################################################################################

# Imports
from urllib.parse import quote

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
        image_url = element.get_attribute('src')
        
        # Close driver
        driver.close()
        
        # Return Data
        return (True, image_url)
    except Exception as error:
        return (False, error)

##########################################################################################################################
