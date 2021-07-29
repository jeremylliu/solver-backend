import cv2
import pytesseract
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'


def readTiles(jpeg):
    nparr = np.frombuffer(jpeg, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    """
    conver to python
    for(int x = 0; x < {matrix}.rows; ++x) {
  for(int y = 0; y < {matrix}.cols; ++y) {
    cv::Vec3b & color = {matrix}.at<cv::Vec3b>(cv::Point(x, y));
    if(color[0] < 5 && color[1] < 5 && color[2] < 5) {
      color[0] = 0;
      color[1] = 0;
      color[2] = 0;
    }
    else {
      color[0] = 255;
      color[1] = 255;
      color[2] = 255;
    }
  }
}"""

    cv2.imshow('image', img_res)
    cv2.waitKey(0)
    words = pytesseract.image_to_string(img_res)
    return words
