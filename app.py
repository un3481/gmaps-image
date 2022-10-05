
##########################################################################################################################

# Imports
from json import dumps
from flask import Flask, request, Response
from urllib.parse import quote, urlencode, urlparse, urlunparse, parse_qs
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

##########################################################################################################################

# Declare WSGI APP
app = Flask('gmaps_app')

# Sets chrome options for Selenium
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_prefs = {}
chrome_options.experimental_options['prefs'] = chrome_prefs
chrome_prefs['profile.default_content_settings'] = {'images': 2}

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
        search_url = 'https://maps.google.com/maps?q=' + quote(address)
        driver = webdriver.Chrome(search_url, options=chrome_options)
        # Search for element
        elements = driver.find_elements_by_css_selector('[jsaction="pane.heroHeaderImage.click"] >img')
        if len(elements) == 0:
            raise Exception('image not found')
        # Get source
        raw_image_url = elements[0].get_attribute('src')
        # Close driver
        driver.close()
        
        # Change image width and height
        parsed_url = urlparse(raw_image_url)
        query = parse_qs(parsed_url.query, keep_blank_values=True)
        query['width'] = [f'{width}']
        query['height'] = [f'{height}']
        parsed_url = parsed_url._replace(query=urlencode(query, True))
        image_url = urlunparse(parsed_url)
        
        # Return Data
        return Response(
            dumps({ 'url': image_url }),
            mimetype='application/json',
            status=200
        )
    except Exception as _error:
        return Response('', status=404)

#################################################################################################################################################
