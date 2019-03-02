import cv2
import numpy as np
import matplotlib.pyplot as plt

def FindPageContour(img, resolution=(640, 480)):
  # Resize and convert to grayscale
  img = cv2.resize(img, resolution)
  img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  # Bilateral filter preserv edges
  img = cv2.bilateralFilter(img, 9, 75, 75)

  # Create black and white image based on adaptive threshold
  img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 4)

  # Median filter clears small details
  img = cv2.medianBlur(img, 11)

  # cv2.imshow('debug', img)
  # cv2.waitKey(0)

  # Add black border in case that page is touching an image border
  img = cv2.copyMakeBorder(img, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=[0, 0, 0])

  edges = cv2.Canny(img, 200, 250)

  # cv2.imshow('canny', edges)
  # cv2.waitKey(0)

  # Getting contours  
  contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

  # Finding contour of biggest rectangle
  # Otherwise return corners of original image
  # Don't forget on our 5px border!
  height = edges.shape[0]
  width = edges.shape[1]
  MAX_COUNTOUR_AREA = (width - 10) * (height - 10)

  # Page fill at least half of image, then saving max area found
  maxAreaFound = MAX_COUNTOUR_AREA * 0.5

  # Saving page contour
  pageContour = np.array([[5, 5], [5, height-5], [width-5, height-5], [width-5, 5]])

  # Go through all contours
  for cnt in contours:
    # Simplify contour
    perimeter = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.03 * perimeter, True)

    # Page has 4 corners and it is convex
    # Page area must be bigger than maxAreaFound 
    if (len(approx) == 4 and
        cv2.isContourConvex(approx) and
        maxAreaFound < cv2.contourArea(approx) < MAX_COUNTOUR_AREA):

      maxAreaFound = cv2.contourArea(approx)
      pageContour = approx

  # Result in pageConoutr (numpy array of 4 points):
  return pageContour

def GetRoi(img):
  original_resolution = img.shape[1], img.shape[0] # Note: shape is rows, cols!
  print('Original resolution:', original_resolution)

  # Downsampled resolution.
  resolution = (640, 480)
  upsample_factor = original_resolution[0] / resolution[0]

  print('Factor:', upsample_factor)

  img_downsampled = cv2.resize(img, resolution)
  outline = FindPageContour(img, resolution=resolution)

  # Scale the outline back to original resolution.
  # NOTE: must be integer coordinates to draw!
  outline_scaled = (upsample_factor * outline).astype(np.int32)

  cv2.drawContours(img, [outline_scaled], 0, (0, 0, 255), 2)
  cv2.imshow('letter', img)
  cv2.waitKey(0)

# img = cv2.imread("/home/milo/Downloads/mail_640_480.png")
# img = cv2.imread("/home/milo/Downloads/handwritten.png")
img = cv2.imread('/home/milo/Downloads/example_mail.jpg')

GetRoi(img)

# cnt = FindPageContour(img, resolution=(640, 480))
# print(cnt)
# cv2.drawContours(img, [4*cnt], 0, (0,0,255), 2)

# cv2.imshow('Letter', img)
# cv2.waitKey(0)
