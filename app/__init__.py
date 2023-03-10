
##########################################################################################################################

# Imports
from flask import Flask, request, Response
from . import google_maps, resize

##########################################################################################################################

# Declare WSGI app
app = Flask('gmaps_image_app')

# Image route
@app.route('/image/', methods=['GET'])
def image():
    try:
        args = request.args
        address = args.get('address', default=None, type=str)
        width = args.get('width', default=None, type=int)
        height = args.get('height', default=None, type=int)
        
        if address == None or width == None or height == None:
            return Response('', status=400)
        
        # launch driver
        driver = google_maps.launch_driver()
        
        # Get URL of image
        ok, url = google_maps.url(driver, address)
        
        # Kill driver
        google_maps.kill_driver(driver)
        
        # Check URL response
        if not ok: return Response('', status=404)
        
        # Download image
        ok, data = resize.download(url)
        if not ok: return Response('', status=404)

        # Transform image
        mimetype, img = data
        img = resize.apply_ratio(img, height, width)
        img = resize.add_padding(img, height, width)
        img = resize.encode(img, mimetype)
        
        # Get image bytes
        img_bytes = img.tobytes()
        
        # Return Data
        return Response(
            img_bytes,
            mimetype = mimetype
        )
    except Exception as error:
        return Response('', status=501)

##########################################################################################################################
