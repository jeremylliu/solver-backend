from image_processing.convert import base64ToImage
from image_processing.read import readTiles


def process(imgStr):
    img = base64ToImage(imgStr)
    board = readTiles(img)
    return board
