import cv2
import pytesseract

img = cv2.imread("/home/milo/Downloads/mail_640_480.png")
cv2.imshow('Letter', img)
cv2.waitKey(0)

output = pytesseract.image_to_string(img, lang='eng')
print(output)
