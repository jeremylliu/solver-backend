import cv2
import numpy as np


def emphasis(img):
    # converts anything that is not black in the image to white
    white = np.array([255, 255, 255])
    newImg = img

    green_range_lower = np.array([0, 160, 0])
    green_range_upper = np.array([255, 255, 255])
    green_wash = cv2.inRange(newImg, green_range_lower, green_range_upper)
    newImg[green_wash == 255] = [0, 0, 0]

    white_range_lower = np.array([40, 0, 0])
    white_range_upper = np.array([255, 255, 255])
    white_wash = cv2.inRange(newImg, white_range_lower, white_range_upper)
    newImg[white_wash == 255] = white

    white_range_lower = np.array([0, 40, 0])
    white_range_upper = np.array([255, 255, 255])
    white_wash = cv2.inRange(newImg, white_range_lower, white_range_upper)
    newImg[white_wash == 255] = white

    white_range_lower = np.array([0, 0, 40])
    white_range_upper = np.array([255, 255, 255])
    white_wash = cv2.inRange(newImg, white_range_lower, white_range_upper)
    newImg[white_wash == 255] = white

    return img
