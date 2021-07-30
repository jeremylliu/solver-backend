import cv2
import pytesseract
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'


def readTiles(jpeg):
    # convert jpeg into np.ndarray that opencv reads
    nparr = np.frombuffer(jpeg, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

    # glare removal
    grayed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mask = cv2.threshold(grayed, 225, 255, cv2.THRESH_BINARY)[1]
    img = cv2.inpaint(img, mask, 21, cv2.INPAINT_TELEA)

    cv2.imshow('image', img)
    cv2.waitKey(0)

    white = np.array([255, 255, 255])

    # convert anything that is not pure black to white
    white_range_lower = np.array([55, 0, 0])
    white_range_upper = np.array([255, 255, 255])
    white_wash = cv2.inRange(img, white_range_lower, white_range_upper)
    img[white_wash == 255] = white

    white_range_lower = np.array([0, 55, 0])
    white_range_upper = np.array([255, 255, 255])
    white_wash = cv2.inRange(img, white_range_lower, white_range_upper)
    img[white_wash == 255] = white

    white_range_lower = np.array([0, 0, 55])
    white_range_upper = np.array([255, 255, 255])
    white_wash = cv2.inRange(img, white_range_lower, white_range_upper)
    img[white_wash == 255] = white

    cv2.imshow('image', img)
    cv2.waitKey(0)

    # cleaning up the image through erosion, closing, and dialation
    kernel3 = np.ones((3, 3), np.uint8)
    kernel2 = np.ones((2, 2), np.uint8)
    kernel1 = np.ones((2, 2), np.uint8)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.bitwise_not(img)

    closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel3)
    dilation = cv2.dilate(closing, kernel2, iterations=3)
    erosion = cv2.erode(dilation, kernel1, iterations=1)

    img = cv2.bitwise_not(erosion)

    cv2.imshow('image', img)
    cv2.waitKey(0)

    # find contours to detect individual letters
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    thresh = cv2.threshold(gray, 127, 255,
                           cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    items = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                             cv2.CHAIN_APPROX_SIMPLE)
    contours = items[0] if len(items) == 2 else items[1]

    img_contour = img.copy()
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if 100 < area < 10000:
            cv2.drawContours(img_contour, contours, i, (0, 0, 255), 2)

    detected = ""
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        ratio = h/w
        area = cv2.contourArea(c)
        base = np.ones(thresh.shape, dtype=np.uint8)
        if ratio > 0.6 and 100 < area < 10000:  # originally .9
            base[y:y+h, x:x+w] = thresh[y:y+h, x:x+w]
            segment = cv2.bitwise_not(base)

            custom_config = r'--oem 3 --psm 10 -c tessedit_char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZwlp" '
            c = pytesseract.image_to_string(segment, config=custom_config)
            detected = detected + c
            print(c)
            cv2.imshow("segment", segment)
            cv2.waitKey(0)

    print("detected: " + detected.strip(' \n\t'))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # custom_config = r'--oem 3 --psm 11 -c tessedit_char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZlpw" '
    # detected = pytesseract.image_to_string(
    #     img, config=custom_config)
    return detected.strip(' \n\t')
