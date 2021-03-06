import cv2
import numpy as np
import matplotlib.pyplot as plt

def FindPageContour(img, resolution):
  # Resize and convert to grayscale
  img = cv2.resize(img, resolution)

  # cv2.imshow('contour', img)
  # cv2.waitKey(0)

  img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  # Bilateral filter preserv edges
  img = cv2.bilateralFilter(img, 9, 75, 75)

  # Create black and white image based on adaptive threshold
  img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 4)

  # Median filter clears small details
  img = cv2.medianBlur(img, 11)

  # Add black border in case that page is touching an image border
  img = cv2.copyMakeBorder(img, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=[0, 0, 0])

  edges = cv2.Canny(img, 200, 250)
  # edges = cv2.Canny(img, 100, 200)

  # cv2.imshow('debug', edges)
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
  maxAreaFound = MAX_COUNTOUR_AREA * 0.1

  # Saving page contour
  pageContour = np.array([[5, 5], [5, height-5], [width-5, height-5], [width-5, 5]])

  print('Num contours:', len(contours))

  # Go through all contours
  for cnt in contours:
    # Simplify contour
    perimeter = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.03 * perimeter, True)

    # Page has 4 corners and it is convex
    # Page area must be bigger than maxAreaFound 
    if (len(approx) == 4 and
        cv2.isContourConvex(approx) and
        maxAreaFound < cv2.contourArea(approx) < 0.9*MAX_COUNTOUR_AREA):

      maxAreaFound = cv2.contourArea(approx)
      pageContour = approx

  # Result in pageConoutr (numpy array of 4 points):
  return pageContour

def order_points(pts):
  # initialzie a list of coordinates that will be ordered
  # such that the first entry in the list is the top-left,
  # the second entry is the top-right, the third is the
  # bottom-right, and the fourth is the bottom-left
  rect = np.zeros((4, 2), dtype = "float32")
 
  # the top-left point will have the smallest sum, whereas
  # the bottom-right point will have the largest sum
  s = pts.sum(axis = 1)
  rect[0] = pts[np.argmin(s)]
  rect[2] = pts[np.argmax(s)]
 
  # now, compute the difference between the points, the
  # top-right point will have the smallest difference,
  # whereas the bottom-left will have the largest difference
  diff = np.diff(pts, axis = 1)
  rect[1] = pts[np.argmin(diff)]
  rect[3] = pts[np.argmax(diff)]
 
  # return the ordered coordinates
  return rect

def four_point_transform(image, pts):
  # obtain a consistent order of the points and unpack them
  # individually
  rect = order_points(pts)
  (tl, tr, br, bl) = rect
 
  # compute the width of the new image, which will be the
  # maximum distance between bottom-right and bottom-left
  # x-coordiates or the top-right and top-left x-coordinates
  widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
  widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
  maxWidth = max(int(widthA), int(widthB))
 
  # compute the height of the new image, which will be the
  # maximum distance between the top-right and bottom-right
  # y-coordinates or the top-left and bottom-left y-coordinates
  heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
  heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
  maxHeight = max(int(heightA), int(heightB))
 
  # now that we have the dimensions of the new image, construct
  # the set of destination points to obtain a "birds eye view",
  # (i.e. top-down view) of the image, again specifying points
  # in the top-left, top-right, bottom-right, and bottom-left
  # order
  dst = np.array([
    [0, 0],
    [maxWidth - 1, 0],
    [maxWidth - 1, maxHeight - 1],
    [0, maxHeight - 1]], dtype = "float32")
 
  # compute the perspective transform matrix and then apply it
  M = cv2.getPerspectiveTransform(rect, dst)
  warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
 
  # return the warped image
  return warped

def BirdsEyeTransform(img, outline_scaled):
  # Scale the outline back to original resolution.
  # NOTE: must be integer coordinates to draw!

  # Convert corners to usable format.
  corners = []
  for i in range(outline_scaled.shape[0]):
    corners.append(outline_scaled[i,:].reshape((2)))
  corners = np.array(corners)

  # cv2.drawContours(img, [corners], 0, (0, 0, 255), 2)
  # cv2.imshow('debug', img)
  # cv2.waitKey(0)

  # Make birds-eye image.
  topview = four_point_transform(img, corners)

  return topview

def PreprocessImage(img):
  # Get corners from the image, and scale them up to the original resolution.
  # NOTE: INPUT IMAGE MUST BE WIDER THAN IT IS TALL (640:480) RATIO!!!!
  # contour_resolution = (1280, 960) # Should be cols x rows.
  # contour_resolution = (1920, 1080)
  contour_resolution = (640, 360)
  original_resolution = img.shape[1], img.shape[0] # Cols x rows.
  upsample_factor = original_resolution[0] / contour_resolution[0]

  # Find the outline of the letter at contour_resolution.
  # Outline points are in (x, y) format which are the width and height dimensions.
  outline = FindPageContour(img, contour_resolution)
  outline_scaled = (upsample_factor * outline).astype(np.int32)

  tf = BirdsEyeTransform(img, outline_scaled)

  # Make the image a more manageable size.
  crop_resolution = (1920, 1080) # Cols x rows.
  img_downsampled = cv2.resize(tf, crop_resolution)

  img_clean = cv2.cvtColor(img_downsampled, cv2.COLOR_BGR2GRAY)

  # Bilateral filter preserv edges
  img_clean = cv2.bilateralFilter(img_clean, 9, 75, 1)

  blurred = cv2.GaussianBlur(img_clean, (5, 5), 0);
  img_clean = cv2.addWeighted(img_clean, 4.0, blurred, -3.0, 0);

  cv2.imshow('debug', img_downsampled)
  # cv2.waitKey(0)

  # Get the 4 crops we care about.
  crops = []

  width = img_clean.shape[1]
  height = img_clean.shape[0]

  crop_w = int(0.5 * width)
  crop_h = int(0.5 * height)

  tl = img_clean[0:crop_h, 0:crop_w]
  tr = img_clean[0:crop_h, width-crop_w:width-1]
  bl = img_clean[height-crop_h : height-1, 0:crop_w]
  br = img_clean[height-crop_h : height-1, width-crop_w:width-1]

  mx = int(width / 2)
  my = int(height / 2)
  mid = img_clean[my-int(crop_h/2):my+int(crop_h/2), mx-int(crop_w/2):mx+int(crop_w/2)]

  return (tl, tr, bl, br, mid)

if __name__ == '__main__':
  
  # img = cv2.imread("/home/milo/Downloads/mail_640_480.png")
  # img = cv2.imread("/home/milo/Downloads/handwritten.png")
  # img = cv2.imread('/home/milo/Downloads/example_mail.png')

  # roi = PreprocessImage(img)

  # for r in roi:
  #   cv2.imshow('roi', r)
  #   cv2.waitKey(0)

  # GetRoi(img)

  # cnt = FindPageContour(img, resolution=(640, 480))
  # print(cnt)
  # cv2.drawContours(img, [4*cnt], 0, (0,0,255), 2)

  # cv2.imshow('Letter', img)
  # cv2.waitKey(0)
  pass
