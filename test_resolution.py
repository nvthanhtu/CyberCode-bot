import cv2
from PIL import ImageGrab
import numpy as np
area = (400,100,800,1200)

printscreen = np.array(ImageGrab.grab(bbox=area))

cv2.imshow("result",printscreen)

cv2.waitKey(0)

cv2.destroyAllWindows()
