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
import base64
from io import BytesIO
import time
import board
import neopixel
import datetime


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


# START: Number Arrays
# ---------------------------------- #

zero = np.array([
    ['#000000', 1, 1, '#000000'],
    [1, '#000000', '#000000', 1],
    [1, '#000000', '#000000', 1],
    [1, '#000000', '#000000', 1],
    ['#000000', 1, 1, '#000000']
])

one = np.array([
    ['#000000', 1, '#000000', '#000000'],
    [1, 1, '#000000', '#000000'],
    ['#000000', 1, '#000000', '#000000'],
    ['#000000', 1, '#000000', '#000000'],
    [1, 1, 1, '#000000']
])

two = np.array([
    ['#000000', 1, 1, '#000000'],
    [1, '#000000', '#000000', 1],
    ['#000000', '#000000', 1, '#000000'],
    ['#000000', 1, '#000000', '#000000'],
    [1, 1, 1, 1]
])

three = np.array([
    ['#000000', 1, 1, '#000000'],
    [1, '#000000', '#000000', 1],
    ['#000000', '#000000', 1, '#000000'],
    [1, '#000000', '#000000', 1],
    ['#000000', 1, 1, '#000000']
])

four = np.array([
    ['#000000', '#000000', 1, '#000000'],
    ['#000000', 1, 1, '#000000'],
    [1, '#000000', 1, '#000000'],
    [1, 1, 1, 1],
    ['#000000', '#000000', 1, '#000000']
])

five = np.array([
    [1, 1, 1, 1],
    [1, '#000000', '#000000', '#000000'],
    [1, 1, 1, '#000000'],
    ['#000000', '#000000', '#000000', 1],
    [1, 1, 1, '#000000']
])

six = np.array([
    ['#000000', 1, 1, '#000000'],
    [1, '#000000', '#000000', '#000000'],
    [1, 1, 1, '#000000'],
    [1, '#000000', '#000000', 1],
    ['#000000', 1, 1, '#000000']
])

seven = np.array([
    [1, 1, 1, '#000000'],
    ['#000000', '#000000', '#000000', 1],
    ['#000000', '#000000', '#000000', 1],
    ['#000000', '#000000', 1, '#000000'],
    ['#000000', '#000000', 1, '#000000']
])

eight = np.array([
    ['#000000', 1, 1, '#000000'],
    [1, '#000000', '#000000', 1],
    ['#000000', 1, 1, '#000000'],
    [1, '#000000', '#000000', 1],
    ['#000000', 1, 1, '#000000']
])

nine = np.array([
    ['#000000', 1, 1, '#000000'],
    [1, '#000000', '#000000', 1],
    ['#000000', 1, 1, 1],
    ['#000000', '#000000', '#000000', 1],
    ['#000000', '#000000', 1, '#000000']
])

numbers_array = [zero, one, two, three, four, five, six, seven, eight, nine]

# END: Number Arrays
# ---------------------------------- #


# START: Converting
# ---------------------------------- #

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % tuple(rgb)

def convert_to_matrix(list):
    converted_matrix = []
    y = 0
    for i in range(len(list)-1, 0, -16):
        row = []
        if y % 2 == 0:
            for j in range(i, i-16, -1):
                row.append(rgb_to_hex(list[j]))
        else:
            for j in range(i-15, i+1, 1):
                row.append(rgb_to_hex(list[j]))
        converted_matrix.append(row)
        y += 1
    return converted_matrix


def generate_matrix():
    matrix = []
    for i in range(16):
        matrix.append([])
        for j in range(16):
            matrix[i].append(0)
    return matrix


# END: Converting
# ---------------------------------- #


# START: Clock
# ---------------------------------- #

def get_time_numbers():
    now = datetime.datetime.now()
    hour = '{:02d}'.format(now.hour)
    minute = '{:02d}'.format(now.minute)

    numbers = [
        numbers_array[int(hour[0])],
        numbers_array[int(hour[1])],
        numbers_array[int(minute[0])],
        numbers_array[int(minute[1])],
    ]
    return numbers


def set_color(number, color):
    return np.where(number == '1', color, number)


def draw_numbers_matrix(numbers, color):
    first   =   set_color(numbers[0], color)
    second  =   set_color(numbers[1], color)
    third   =   set_color(numbers[2], color)
    fourth  =   set_color(numbers[3], color)

    converted_matrix = convert_to_matrix(pixels)
    
    pixel_array = np.matrix(np.array(converted_matrix))
    # first
    pos_x = 4
    pos_y = 2
    pixel_array[pos_y:pos_y+first.shape[0],pos_x:pos_x+first.shape[1]] = first
    
    # second
    pos_x = 9
    pos_y = 2
    pixel_array[pos_y:pos_y+second.shape[0],pos_x:pos_x+second.shape[1]] = second

    # third
    pos_x = 4
    pos_y = 9
    pixel_array[pos_y:pos_y+third.shape[0],pos_x:pos_x+third.shape[1]] = third

    # fourth
    pos_x = 9
    pos_y = 9
    pixel_array[pos_y:pos_y+fourth.shape[0],pos_x:pos_x+fourth.shape[1]] = fourth
    

    pixel_array = pixel_array.tolist()

    rgb_matrix = convert_to_RGB(pixel_array)
    converted_matrix = change_matrix_layout(rgb_matrix)
    update_matrix(converted_matrix)


def clock_task():
    global time_numbers, clock_active
    while clock_active:
        print('check')
        if not np.array_equal(time_numbers, get_time_numbers()):
            time_numbers = get_time_numbers()
            draw_numbers_matrix(time_numbers, '#ffffff')
        time.sleep(1)





# END: Clock
# ---------------------------------- #


# START: Encoding / Decoding
# ---------------------------------- #

def encode_image_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    encoded = base64.b64encode(buffered.getvalue())
    return encoded


def decode_image_base64(image_base64):
    image = Image.open(BytesIO(base64.b64decode(image_base64)))
    return image

# END: Encoding / Decoding
# ---------------------------------- #

# Creates an 16x16 PNG from a pixel matrix
# Sends it back to the frontend als base64
def convert_to_image(pixels):
    for i in range(len(pixels)):
        for j in range(len(pixels[i])):
            rgb = (0, 0, 0)
            if pixels[i][j] != '':
                rgb = ImageColor.getcolor(pixels[i][j], "RGB")
            pixels[i][j] = rgb
            
    array = np.array(pixels, dtype=np.uint8)
    new_image = Image.fromarray(array)
    buffered = BytesIO()
    new_image.save(buffered, format="PNG")
    image = base64.b64encode(buffered.getvalue())
    return image, pixels

  
# Draw a new 16x16 image on the led matrix
# update: matrix array
def update_matrix(update):
    for i in range(len(update)):
        pixels[i] = (update[i][0], update[i][1], update[i][2])
    pixels.show()

    print('updated matrix...')

# Changes the matrix so that it can be drawn easaly
# The matrix (0|0) starts in the bottom left corner
# and continues from left to right
def change_matrix_layout(change):
    converted = []
    change = change[::-1]

    for i in range(len(change)):
        if i % 2 == 1:
            converted += change[i][::-1]
        else:
            converted += change[i]

    for i in range(len(converted)):
        converted[i] = list(converted[i])
    
    print('changed matrix layout...')
    return converted

# Converts the HEX color to RGB
def convert_to_RGB(pixels):
    for i in range(len(pixels)):
        for j in range(len(pixels[i])):
            rgb = (0, 0, 0)
            if pixels[i][j] != '':
                rgb = ImageColor.getcolor(pixels[i][j], "RGB")
            pixels[i][j] = rgb

    print('converted matrix to RGB')
    return pixels


def resize_image(image_base64):
    image = decode_image_base64(image_base64)
    image_resized = image.resize((16,16), resample=Image.BILINEAR)
    image_resized = image_resized.rotate(180)
    image_resized.save('image.png')
    return encode_image_base64(image_resized)


def draw_image_on_matrix(image_resized):
    image = Image.open('image.png', 'r')
    width, height = image.size
    pixel_values = list(image.getdata())
    
    try:
        converted_matrix = change_matrix_layout([pixel_values])
        update_matrix(converted_matrix)
    except:
        return False
    return True

def send_http_response(data):
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/image/matrix', methods=['POST'])
def post_new_image():
    data = request.get_json()

    encoded_image = data['image']
    
    encoded_image = encoded_image[22:]
    resized_image = resize_image(encoded_image)
    success = draw_image_on_matrix(resize_image)
    
    return send_http_response({'success': success})


@app.route('/matrix', methods=['POST'])
def post_new_matrix():
    data = request.get_json()

    global clock_active
    clock_active = False

    new_matrix = data['matrix']
    rgb_matrix = convert_to_RGB(new_matrix)
    converted_matrix = change_matrix_layout(rgb_matrix)
    update_matrix(converted_matrix)

    # draw_numbers_matrix(get_time_numbers(), '#4287f5')
    
    return send_http_response({'success': True})


@app.route('/clock', methods=['POST'])
def start_clock():
    global clock_active
    clock_active = True
    thread = Thread(target=clock_task)
    thread.daemon = True
    thread.start()
    return send_http_response({'started': True})


@app.route('/image', methods=['POST'])
def image():
    data = request.get_json()
    raw_data = data['image']

    if data['save'] == True:

        return_data = [[0 for x in range(16)] for y in range(16)] 
        for i in range(len(raw_data)):
            for j in range(len(raw_data[i])):
                return_data[i][j] = raw_data[i][j]
        
        image, _ = convert_to_image(raw_data)

        return jsonify(
        image=image.decode("utf-8"),
        frame=return_data,
        )
    else:
        print('frame')
        image, pixels = convert_to_image(raw_data)
        return jsonify(
            image=image.decode("utf-8"),
            frame=pixels,
        )


@app.route('/brightness', methods=['POST'])
def post_new_brightness():
    data = request.get_json()
    brightness_percentage = data['brightness']

    brightness = (0.8 * brightness_percentage) / 100
    if brightness > 0.8: brightness = 0.8

    pixels.brightness = brightness
    pixels.show()

    return send_http_response({
        'success': True,
        'brightness': brightness_percentage
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0')