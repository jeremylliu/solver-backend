import cv2
import numpy as np


def clarify(img):

    # filters the image and cleans it up
    kernel1 = np.ones((2, 2), np.uint8)
    kernel2 = np.ones((2, 2), np.uint8)
    kernel3 = np.ones((3, 3), np.uint8)

    # newImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # newImg = cv2.bitwise_not(newImg)
    newImg = img

    closing = cv2.morphologyEx(newImg, cv2.MORPH_CLOSE, kernel3)
    dilation = cv2.dilate(closing, kernel2, iterations=3)
    opening = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel3)
    erosion = cv2.erode(opening, kernel1, iterations=1)

    # newImg = cv2.bitwise_not(erosion)

    return erosion
