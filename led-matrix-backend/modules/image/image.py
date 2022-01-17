import numpy as np
from PIL import Image, ImageColor
import modules.utils.base64 as base64
import modules.utils.matrix as matrix


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
    image = base64.encode_image_base64(new_image)

    return image, pixels


def resize_image(image_base64):
    image = base64.decode_image_base64(image_base64)
    image_resized = image.resize((16,16), resample=Image.BILINEAR)
    image_resized = image_resized.rotate(180)
    image_resized.save('image.png')
    return base64.encode_image_base64(image_resized)


def image_to_matrix(image_resized):
    image = Image.open('image.png', 'r')
    width, height = image.size
    pixel_values = list(image.getdata())
    
    try:
        converted_matrix = matrix.matrix_to_led_list([pixel_values])
    except:
        return False
    return True, converted_matrix