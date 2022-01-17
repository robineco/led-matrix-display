import time
import datetime
import numpy as np

import modules.clock.numbers as numbers
import modules.utils.matrix as matrix


clock_active = False
time_numbers = []


def get_time_numbers():
    now = datetime.datetime.now()
    hour = '{:02d}'.format(now.hour)
    minute = '{:02d}'.format(now.minute)
    
    time_numbers = [
        numbers.numbers_array[int(hour[0])],
        numbers.numbers_array[int(hour[1])],
        numbers.numbers_array[int(minute[0])],
        numbers.numbers_array[int(minute[1])],
    ]
    return time_numbers


def set_color(number, color):
    return np.where(number == '1', color, number)


def create_numbers_matrix(numbers, color, pixels):
    first   =   set_color(numbers[0], color)
    second  =   set_color(numbers[1], color)
    third   =   set_color(numbers[2], color)
    fourth  =   set_color(numbers[3], color)

    converted_matrix = matrix.list_to_matrix(pixels)
    
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

    rgb_matrix = matrix.matrix_to_RGB(pixel_array)
    converted_matrix = matrix.matrix_to_led_list(rgb_matrix)
    return converted_matrix
