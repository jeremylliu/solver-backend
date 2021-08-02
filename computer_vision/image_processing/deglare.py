import cv2


def deglare(img):
    # removes the glare off an image
    # glare removal
    grayed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mask = cv2.threshold(grayed, 225, 255, cv2.THRESH_BINARY)[1]
    newImg = cv2.inpaint(img, mask, 21, cv2.INPAINT_TELEA)
    return newImg
