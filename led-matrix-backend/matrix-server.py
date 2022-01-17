from nis import match
from pickle import FALSE
from tkinter.tix import Tree
from flask import Flask, request
from flask import jsonify
from flask_cors import CORS
from threading import Thread
from PIL import Image, ImageColor
from threading import Thread
import numpy as np

from io import BytesIO
import time
import board
import neopixel
import datetime

import modules.utils.matrix as matrix
import modules.utils.converter as converter
import modules.utils.base64 as base64
import modules.utils.http as http
import modules.clock.clock as clock
import modules.image.image as image_service

#export FLASK_ENV=development
#export FLASK_APP=matrix-server.py

pixel_pin = board.D21
num_pixels = 256
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.05, auto_write=False, pixel_order=ORDER
)


pixels.fill((0, 0, 0))
pixels.show()


app = Flask(__name__)
cors = CORS(app)


clock_active = False
time_numbers = []


# START: Clock
# ---------------------------------- #

def clock_task():
    global time_numbers, clock_active
    while clock_active:
        if not np.array_equal(time_numbers, clock.get_time_numbers()):
            time_numbers = clock.get_time_numbers()
            clock_matrix = clock.create_numbers_matrix(time_numbers, '#ffffff', pixels)
            update_matrix(clock_matrix)
        time.sleep(1)

# END: Clock
# ---------------------------------- #

  
# Draw a new 16x16 image on the led matrix
# update: matrix array
def update_matrix(update):
    for i in range(len(update)):
        pixels[i] = (update[i][0], update[i][1], update[i][2])
    pixels.show()


@app.route('/image/matrix', methods=['POST'])
def post_new_image():
    data = request.get_json()

    encoded_image = data['image']
    
    encoded_image = encoded_image[22:]
    resized_image = image_service.resize_image(encoded_image)
    success, matrix = image_service.image_to_matrix(resized_image)
    update_matrix(matrix)
    
    return http.send_http_response({'success': success})


@app.route('/matrix', methods=['POST'])
def post_new_matrix():
    data = request.get_json()

    global clock_active
    clock_active = False

    new_matrix = data['matrix']
    converted_matrix = matrix.convert_matrix(new_matrix)
    update_matrix(converted_matrix)
    
    return http.send_http_response({'success': True})


@app.route('/clock', methods=['POST'])
def start_clock():
    global clock_active
    clock_active = True
    thread = Thread(target=clock_task)
    thread.daemon = True
    thread.start()
    return http.send_http_response({'started': True})


@app.route('/image', methods=['POST'])
def image():
    data = request.get_json()
    raw_data = data['image']

    if data['save'] == True:

        return_data = [[0 for x in range(16)] for y in range(16)] 
        for i in range(len(raw_data)):
            for j in range(len(raw_data[i])):
                return_data[i][j] = raw_data[i][j]
        
        image, _ = image_service.convert_to_image(raw_data)

        return http.send_http_response({
            'image': image.decode("utf-8"),
            'frame': return_data,
        })
    else:
        image, pixels = image_service.convert_to_image(raw_data)

        return http.send_http_response({
            'image': image.decode("utf-8"),
            'frame': pixels,
        })


@app.route('/brightness', methods=['POST'])
def post_new_brightness():
    data = request.get_json()
    brightness_percentage = data['brightness']

    brightness = (0.8 * brightness_percentage) / 100
    if brightness > 0.8: brightness = 0.8

    pixels.brightness = brightness
    pixels.show()

    return http.send_http_response({
        'success': True,
        'brightness': brightness_percentage
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0')