import cv2

from preprocess import *
from ocr import *

if __name__ == '__main__':
  img = cv2.imread('/home/milo/Downloads/example_mail.png')

  roi = PreprocessImage(img)

  for r in roi:
    text = DetectText(r)
    print(text)
    
    cv2.imshow('roi', r)
    cv2.waitKey(0)
