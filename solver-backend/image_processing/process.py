from convert import base64ToImage
from read import readTiles


def process(imgStr):
    img = base64ToImage(imgStr)
    board = readTiles(img)
    return board
