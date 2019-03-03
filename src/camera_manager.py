import cv2

class CameraManager(object):
  def __init__(self, devicenum = 1):
    self.devicenum = devicenum
    self.cap = cv2.VideoCapture(self.devicenum)

    if (not self.cap.isOpened()):
      print('ERROR: Could not open webcam (%d)' % self.devicenum)

  def Capture(self):
    for i in range(4):
      self.cap.grab()
    ret, frame = self.cap.read()
    return frame

  def Shutdown(self):
    self.cap.release()
    cv2.destroyAllWindows()

  def Stream(self):
    while(True):
      # Capture frame-by-frame
      ret, frame = self.cap.read()

      # Our operations on the frame come here
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

      # Display the resulting frame
      cv2.imshow('frame', gray)
      if cv2.waitKey(1) & 0xFF == ord('q'):
          break
