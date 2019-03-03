import cv2
import pytesseract
import time

import numpy as np
import matplotlib.pyplot as plt

def DetectText(img):
  """
  Downsamples an image to the desired resolution then runs OCR.
  """
  output = pytesseract.image_to_string(img)
  return output

if __name__ == '__main__':
  # img = cv2.imread("/home/milo/Downloads/mail_640_480.png")
  # img = cv2.imread("/home/milo/Downloads/handwritten.png")
  # img = cv2.imread("/home/milo/Downloads/cropped_mail.png")
  # img = cv2.imread("/home/milo/Downloads/example_mail.jpg")

  # cv2.imshow('img', img)
  # cv2.waitKey(0)

  t0 = time.time()
  # output = pytesseract.image_to_string(img, lang='eng')
  text = DetectText(img)
  end = time.time()

  print('Took %f sec', (end - t0))

  print(text)
