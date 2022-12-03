
##########################################################################################################################

# Imports
import requests
import numpy as np
import math
import cv2

##########################################################################################################################

def download(url: str):
    try:
        res = requests.get(url)

        # Check status
        if res.status_code != 200:
            raise Exception('Could not download file')

        # Check mimetype
        mimetype = res.headers.get('content-type', default='').lower()
        if mimetype not in ['image/png', 'image/jpeg', 'image/gif']:
            raise Exception('Invalid MIME type')

        # Decode image
        npimg = np.fromstring(res.content, np.uint8)
        img: cv2.Mat = cv2.imdecode(npimg, cv2.IMREAD_ANYCOLOR)
        
        # Return data
        return (True, (mimetype, img))
    except Exception as error:
        return (False, error)


##########################################################################################################################

def apply_ratio(img: cv2.Mat, height: int, width: int) -> cv2.Mat:
    h, w = img.shape[:2]
    
    # Calculate image ratio
    ratio = w / h
    
    # Check if resulting image will be larger or smaller than original
    larger = h > height or w > width
    interp = cv2.INTER_AREA if larger else cv2.INTER_CUBIC
    
    # Calculate target image size
    w = width
    h = math.floor(w / ratio)
    if h > height:
        h = height
        w = math.floor(h * ratio)
    
    # Resize image preserving ratio
    return cv2.resize(
        img,
        (w, h),
        interpolation = interp
    )

##########################################################################################################################

def add_padding(img: cv2.Mat, height: int, width: int) -> cv2.Mat:
    h, w = img.shape[:2]
    
    # Calculate padding
    pad_vert = round(abs(height - h) / 2)
    pad_horz = round(abs(width - w) / 2)
    pad_odd_vert = height - h - (pad_vert * 2)
    pad_odd_horz = width - w - (pad_horz * 2)
    
    # Add reflected padding and blur
    blurred_img = cv2.GaussianBlur(
        cv2.copyMakeBorder(
            img,
            pad_vert,
            pad_vert + pad_odd_vert,
            pad_horz,
            pad_horz + pad_odd_horz,
            borderType = cv2.BORDER_REFLECT
        ),
        (15, 15),
        7
    )

    # Apply blur only to borders
    blurred_img[pad_vert:pad_vert+h-1, pad_horz:pad_horz+w-1] = img[0:h-1, 0:w-1]
    
    # Return data
    return blurred_img

##########################################################################################################################

def encode(img: cv2.Mat, mimetype: str) -> cv2.Mat:
    # Get file extension
    ext = mimetype.replace('image/', '')
    if ext == 'jpeg': ext = 'jpg'
    
    # Encode image to target format
    _, enc = cv2.imencode(f'.{ext}', img)
    
    # Retrun data
    return enc
        
##########################################################################################################################
