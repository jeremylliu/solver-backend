import cv2
import numpy as np


def clean(img):
    # removes anything that was not filtered by emphasize
    black_range_lower = np.array([0, 0, 0])
    black_range_upper = np.array([1, 1, 1])
    black_wash = cv2.inRange(img, black_range_lower, black_range_upper)
    img[black_wash == 255] = [0, 255, 0]

    color_range_lower = np.array([0, 0, 0])
    color_range_upper = np.array([255, 254, 255])
    color_wash = cv2.inRange(img, color_range_lower, color_range_upper)
    img[color_wash == 255] = [255, 255, 255]

    color_wash = cv2.inRange(img, np.array([0, 254, 0]), np.array([0, 255, 0]))
    img[color_wash == 255] = [0, 0, 0]

    return img
