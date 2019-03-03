import cv2

from preprocess import *
from ocr import *
from camera_manager import *

def Test():
  img = cv2.imread('/home/milo/Downloads/example_mail.png')
  # img = cv2.imread('/home/milo/Downloads/handwritten.png')
  # img = cv2.imread('/home/milo/Downloads/better.jpg')

  roi = PreprocessImage(img)

  for r in roi:
    text = DetectText(r)
    print(text)
    
    cv2.imshow('roi', r)
    cv2.waitKey(0)

# if __name__ == '__main__':
#   cm = CameraManager(0)

#   img = cm.Capture()

#   all_text = []
#   roi = PreprocessImage(img)
  
#   for r in roi:
#     text = DetectText(r)
#     print(text)

#     all_text.append(text)
    
#     cv2.imshow('roi', r)
#     cv2.waitKey(0)

#   print(all_text)

#   cm.Shutdown()

Test()
