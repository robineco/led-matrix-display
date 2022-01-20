import modules.utils.matrix as matrix
import modules.image.image as image_service


def post_handler_draw_matrix(data):
    new_matrix = data['matrix']
    converted_matrix = matrix.convert_matrix(new_matrix)
    return converted_matrix


def post_handler_draw_image(data):
    encoded_image = data['image']
    encoded_image = encoded_image[22:]
    resized_image = image_service.resize_image(encoded_image)
    success, matrix = image_service.image_to_matrix(resized_image)
    return success, matrix


def post_handler_create_image(data):
    raw_data = data['image']

    if data['save'] == True:

        return_data = [[0 for x in range(16)] for y in range(16)] 
        for i in range(len(raw_data)):
            for j in range(len(raw_data[i])):
                return_data[i][j] = raw_data[i][j]
        
        image, _ = image_service.convert_to_image(raw_data)

        return image, return_data

    else:
        image, pixels = image_service.convert_to_image(raw_data)
        
        return image, pixels


def post_handler_brightness(data):
    brightness_percentage = data['brightness']
    brightness = (0.8 * brightness_percentage) / 100
    if brightness > 0.8: brightness = 0.8
    return brightness, brightness_percentage

