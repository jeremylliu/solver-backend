import base64
import io


def base64ToImage(imageStr):
    # takes in a base64 imageStr and returns a jpeg object
    imageStr = imageStr[22:]
    img = io.BytesIO(base64.b64decode(imageStr))
    return img.read()
