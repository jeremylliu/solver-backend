import math

import cv2
import numpy as np

from deskew import determine_skew


def deskew(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    angle = determine_skew(gray)
    if(angle < -45):
        angle += 90

    old_width, old_height = img.shape[:2]
    angle_radian = math.radians(angle)
    width = abs(np.sin(angle_radian) * old_height) + \
        abs(np.cos(angle_radian) * old_width)
    height = abs(np.sin(angle_radian) * old_width) + \
        abs(np.cos(angle_radian) * old_height)

    image_center = tuple(np.array(img.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    rot_mat[1, 2] += (width - old_width) / 2
    rot_mat[0, 2] += (height - old_height) / 2
    newImg = cv2.warpAffine(
        img, rot_mat, (int(round(height)), int(round(width))), borderValue=(0, 0, 0), borderMode=cv2.BORDER_REPLICATE)
    return newImg


def olddeskew(img):
    # determine image skew
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    contoursSkew = cv2.findContours(
        thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
    contoursSkew = sorted(contoursSkew, key=cv2.contourArea, reverse=True)
    largestContour = contoursSkew[0]
    minAreaRect = cv2.minAreaRect(largestContour)
    angle = minAreaRect[-1]
    angle = angle - 90

    # rotate image around center to correct skew
    rotatedImg = img.copy()
    (h, w) = rotatedImg.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotatedImg = cv2.warpAffine(
        rotatedImg, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    img = rotatedImg

    return img
