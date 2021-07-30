import cv2
import numpy as np


def emphasis(img):
    # converts anything that is not black in the image to white
    white = np.array([255, 255, 255])
    newImg = img

    white_range_lower = np.array([65, 0, 0])
    white_range_upper = np.array([255, 255, 255])
    white_wash = cv2.inRange(newImg, white_range_lower, white_range_upper)
    newImg[white_wash == 255] = white

    white_range_lower = np.array([0, 55, 0])
    white_range_upper = np.array([255, 255, 255])
    white_wash = cv2.inRange(newImg, white_range_lower, white_range_upper)
    newImg[white_wash == 255] = white

    white_range_lower = np.array([0, 0, 65])
    white_range_upper = np.array([255, 255, 255])
    white_wash = cv2.inRange(newImg, white_range_lower, white_range_upper)
    newImg[white_wash == 255] = white

    return img
