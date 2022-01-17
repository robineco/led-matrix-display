from PIL import Image
from io import BytesIO
import base64


def encode_image_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    encoded = base64.b64encode(buffered.getvalue())
    return encoded


def decode_image_base64(image_base64):
    image = Image.open(BytesIO(base64.b64decode(image_base64)))
    return image