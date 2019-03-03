import cv2

from preprocess import *
from ocr import *
from camera_manager import *

def TestStatic():
  # img = cv2.imread('/home/milo/Downloads/example_mail.png')
  # img = cv2.imread('/home/milo/Downloads/handwritten.png')
  img = cv2.imread('/home/milo/Downloads/better.jpg')

  roi = PreprocessImage(img)

  for r in roi:
    text = DetectText(r)
    print(text)
    
    cv2.imshow('roi', r)
    cv2.waitKey(0)

TestStatic()
