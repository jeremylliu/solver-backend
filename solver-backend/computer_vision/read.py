import cv2
import pytesseract
import numpy as np
from computer_vision.image_processing.deglare import deglare
from computer_vision.image_processing.emphasis import emphasis
from computer_vision.image_processing.clarify import clarify
from computer_vision.image_processing.deskew import deskew

pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'


def readTiles(jpeg):
    # convert jpeg into np.ndarray that opencv reads
    nparr = np.frombuffer(jpeg, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

    # # clean up the image to become more readable for tesseract
    img = cv2.GaussianBlur(img, (7, 7), 1)
    # img = deglare(img)
    img = emphasis(img)
    img = clarify(img)
    img = deskew(img)

    black_range_lower = np.array([0, 0, 0])
    black_range_upper = np.array([1, 1, 1])
    black_wash = cv2.inRange(img, black_range_lower, black_range_upper)
    img[black_wash == 255] = [0, 255, 0]

    color_range_lower = np.array([0, 0, 0])
    color_range_upper = np.array([255, 254, 255])
    color_wash = cv2.inRange(img, color_range_lower, color_range_upper)
    img[color_wash == 255] = [255, 255, 255]

    cv2.imshow('cleaned img', img)
    cv2.waitKey(0)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # """
    # TRYTING TO GET CONTOUR FOR SHAPE
    thresh = cv2.threshold(gray, 127, 255,
                           cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(
            cnt, 0.05 * cv2.arcLength(cnt, True), True)
        cv2.drawContours(img, [cnt], 0, (0, 0, 255), 5)
        # Approximate what type of shape this is
        if len(approx) == 4 and area > 8000:
            x, y, w, h = cv2.boundingRect(cnt)
            print("THIS SHAPE", x, y, area)
            cv2.putText(img, "square", (x, y),
                        cv2.FONT_HERSHEY_COMPLEX, .7, (255, 0, 255), 1)
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.imshow('rotated img', img)
            cv2.waitKey(0)
    # """

    # find contours to detect individual letters
    thresh = cv2.threshold(gray, 127, 255,
                           cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)

    # draw the contours
    img_contour = img.copy()
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if 100 < area < 3000:
            cv2.drawContours(img_contour, contours, i, (0, 0, 255), 2)

    # sort the contours
    boundingBoxes = [cv2.boundingRect(c) for c in contours]
    (contours, boundingBoxes) = zip(*sorted(zip(contours, boundingBoxes),
                                            key=lambda b: b[1][1], reverse=True))

    # read the contours into text
    detected = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        ratio = h/w
        area = cv2.contourArea(c)
        base = np.ones(thresh.shape, dtype=np.uint8)
        if ratio > 0.9 and 100 < area < 3000:
            base[y:y+h, x:x+w] = thresh[y:y+h, x:x+w]
            segment = cv2.bitwise_not(base)

            custom_config = r'--oem 3 --psm 10 -c tessedit_char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" '
            c = pytesseract.image_to_string(
                segment, config=custom_config).strip(' \n\t\x0c')
            detected.append(c)
            print(c, [x, y, w, h])
            cv2.imshow("segment", segment)
            cv2.waitKey(0)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return detected
