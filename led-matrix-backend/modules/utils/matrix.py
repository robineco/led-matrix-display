from PIL import ImageColor
import modules.utils.converter as converter


def list_to_matrix(list):
    converted_matrix = []
    y = 0
    for i in range(len(list)-1, 0, -16):
        row = []
        if y % 2 == 0:
            for j in range(i, i-16, -1):
                row.append(converter.rgb_to_hex(list[j]))
        else:
            for j in range(i-15, i+1, 1):
                row.append(converter.rgb_to_hex(list[j]))
        converted_matrix.append(row)
        y += 1
    return converted_matrix


def matrix_to_RGB(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            rgb = (0, 0, 0)
            if matrix[i][j] != '':
                rgb = ImageColor.getcolor(matrix[i][j], "RGB")
            matrix[i][j] = rgb

    return matrix


# Changes the matrix so that it can be drawn easaly
# The matrix (0|0) starts in the bottom left corner
# and continues from left to right
def matrix_to_led_list(matrix):
    converted = []
    matrix = matrix[::-1]

    for i in range(len(matrix)):
        if i % 2 == 1:
            converted += matrix[i][::-1]
        else:
            converted += matrix[i]

    for i in range(len(converted)):
        converted[i] = list(converted[i])
    
    return converted


def convert_matrix(matrix):
    rgb_matrix = matrix_to_RGB(matrix)
    return matrix_to_led_list(rgb_matrix)