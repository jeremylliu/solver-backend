import cv2
import pytesseract
import numpy as np
from computer_vision.image_processing.deglare import deglare
from computer_vision.image_processing.emphasis import emphasis
from computer_vision.image_processing.clarify import clarify
from computer_vision.image_processing.deskew import deskew
from computer_vision.image_processing.clean import clean

pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'


def readTiles(jpeg):
    # convert jpeg into np.ndarray that opencv reads
    nparr = np.frombuffer(jpeg, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

    # clean up the image to become more readable for tesseract
    img = cv2.GaussianBlur(img, (7, 7), 1)
    # img = deglare(img)
    img = emphasis(img)
    img = clarify(img)
    img = deskew(img)

    # removes some background noise
    img = clean(img)

    # cv2.imshow('cleaned img', img)
    # cv2.waitKey(0)
    print("processed image")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # detects the contour for the playing grid
    thresh = cv2.threshold(gray, 0, 255,
                           cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)

    max_area = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(
            cnt, 0.05 * cv2.arcLength(cnt, True), True)
        if len(approx) == 4 and area > max_area:
            x, y, w, h = cv2.boundingRect(cnt)
            crop = img[y:y+h, x:x+w]
            max_area = area

    img = cv2.bitwise_not(crop)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # cv2.imshow('crop', img)
    # cv2.waitKey(0)
    print("found grid")

    # find contours to detect individual letters
    thresh = cv2.threshold(gray, 127, 255,
                           cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP,
                                           cv2.CHAIN_APPROX_SIMPLE)

    # read the contours into text
    detected = []
    custom_config = r'--oem 3 --psm 10 -c tessedit_char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZl" '

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 2500:
            x, y, w, h = cv2.boundingRect(cnt)
            approx = cv2.approxPolyDP(
                cnt, 0.05 * cv2.arcLength(cnt, True), True)

        if len(approx) == 4 and area > 2500 and area < 10000:
            segment = img[y+5:y+h-10, x+5:x+w-10]
            kernel = np.ones((4, 4), np.uint8)
            segment = cv2.dilate(segment, kernel, iterations=1)
            segment = cv2.GaussianBlur(segment, (5, 5), 1)

            c = pytesseract.image_to_string(
                segment, config=custom_config).strip(' \n\t\x0c')
            if c == "":
                c = "I"
            if(len(c) <= 1):
                detected.append({"guess": c, "x": x, "y": y})
                # print(c, [x, y, w, h], area)
                # cv2.imshow("segment", segment)
                # cv2.waitKey(0)

    print("found letters")

    # sort results
    yRange = []
    yDic = {}
    exists = False
    for guess in detected:
        if len(yRange) == 0:
            yRange.append(guess["y"])
            yDic[guess["y"]] = [guess]
        else:
            for y in yRange:
                if abs(y - guess["y"]) < 15:
                    exists = True
                    yDic[y].append(guess)
                    break
            if exists == False:
                yRange.append(guess["y"])
                yDic[guess["y"]] = [guess]
            exists = False

    board = []
    for y in reversed([*yDic]):
        if len(yDic[y]) == 4:
            yDic[y] = sorted(yDic[y], key=lambda i: i['x'], reverse=False)
            for value in yDic[y]:
                board.append(value['guess'])

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return board
