
##########################################################################################################################

# Imports
from re import sub
from json import dumps
from flask import Flask, request, Response
from urllib.parse import quote, urlencode, urlparse, urlunparse, parse_qs

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

##########################################################################################################################

# Declare WSGI app
app = Flask('gmaps_app')

# Sets options for Firefox Selenium
firefox_options = Options()
firefox_options.add_argument('-headless')

# Regular expresion for resizing usercontent images
usrctt_re = r'=w(\d+)-h(\d+)'

#################################################################################################################################################

@app.route('/image/')
def gmaps_image():
    try:
        args = request.args
        address = args.get('address', default=None, type=str)
        width = args.get('width', default=None, type=int)
        height = args.get('height', default=None, type=int)
        
        if address == None or width == None or height == None:
            return Response('', status=400)
        
        # Launch driver
        driver = webdriver.Firefox(options=firefox_options)
        driver.get('https://maps.google.com/maps?q=' + quote(address))
        # Search for element
        element: WebElement = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[jsaction="pane.heroHeaderImage.click"] >img')
            )
        )
        # Get source
        raw_image_url = element.get_attribute('src')
        # Close driver
        driver.close()
        
        # Change image width and height
        image_url = ''
        if 'googleusercontent' in raw_image_url:
            resized = f'=w{width}-h{height}'
            image_url = sub(usrctt_re, resized, raw_image_url)
        else:
            parsed_url = urlparse(raw_image_url)
            query = parse_qs(parsed_url.query, keep_blank_values=True)
            query['w'] = [f'{width}']
            query['h'] = [f'{height}']
            parsed_url = parsed_url._replace(query=urlencode(query, True))
            image_url = urlunparse(parsed_url)
        
        # Return Data
        return Response(
            dumps({ 'url': image_url }),
            mimetype='application/json',
            status=200
        )
    except Exception as error:
        return Response('', status=404)

#################################################################################################################################################
