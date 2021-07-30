from computer_vision.convert import base64ToImage
from computer_vision.read import readTiles


def process(imgStr):
    img = base64ToImage(imgStr)
    board = readTiles(img)
    return board
