from flask import Flask, request
from flask_cors import CORS
from threading import Thread
import numpy as np

import time
import board
import neopixel

import modules.http.controller as controller
import modules.utils.matrix as matrix
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


# START: Matrix operations
# ---------------------------------- #

def clear_matrix_led():
    pixels.fill((0, 0, 0))


def draw_matrix_led(update):
    for i in range(len(update)):
        pixels[i] = (update[i][0], update[i][1], update[i][2])
    pixels.show()

# END: Matrix operations
# ---------------------------------- #


# START: Clock
# ---------------------------------- #

def disable_clock():
    global clock_active, time_numbers
    clock_active = False
    time_numbers = []


def enable_clock():
    global clock_active, time_numbers
    clock_active = True
    time_numbers = []


def clock_task():
    global time_numbers, clock_active
    while clock_active:
        if not np.array_equal(time_numbers, clock.get_time_numbers()):
            time_numbers = clock.get_time_numbers()
            clock_matrix = clock.create_numbers_matrix(time_numbers, '#ffffff', pixels)
            draw_matrix_led(clock_matrix)
        time.sleep(1)

# END: Clock
# ---------------------------------- #



@app.route('/image/matrix', methods=['POST'])
def post_new_image():
    data = request.get_json()

    disable_clock()

    success, matrix = controller.post_handler_draw_image(data)
    draw_matrix_led(matrix)
    
    return http.send_http_response({'success': success})


@app.route('/matrix', methods=['POST'])
def post_new_matrix():
    data = request.get_json()

    disable_clock()

    converted_matrix = controller.post_handler_draw_matrix(data)
    draw_matrix_led(converted_matrix)
    
    return http.send_http_response({'success': True})


@app.route('/clock', methods=['POST'])
def start_clock():
    clear_matrix_led()
    enable_clock()

    thread = Thread(target=clock_task)
    thread.daemon = True
    thread.start()

    return http.send_http_response({'started': True})


@app.route('/image', methods=['POST'])
def image():
    data = request.get_json()

    image, matrix = controller.post_handler_create_image(data)

    return http.send_http_response({
            'image': image.decode("utf-8"),
            'frame': matrix,
        })


@app.route('/brightness', methods=['POST'])
def post_new_brightness():
    data = request.get_json()
    
    brightness, percentage = controller.post_handler_brightness(data)

    pixels.brightness = brightness
    pixels.show()

    return http.send_http_response({
        'success': True,
        'brightness': percentage
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0')