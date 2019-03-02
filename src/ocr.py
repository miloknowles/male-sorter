import cv2
import pytesseract
import time

import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("/home/milo/Downloads/mail_640_480.png")
img = cv2.imread("/home/milo/Downloads/handwritten.png")

t0 = time.time()
output = pytesseract.image_to_string(img, lang='eng')
end = time.time()

print('Took %f sec', (end - t0))

print(output)
