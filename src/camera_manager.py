import cv2

class CameraManager(object):
  def __init__(self, devicenum = 1):
    self.devicenum = devicenum
    self.cap = cv2.VideoCapture(self.devicenum)

    if (not self.cap.isOpened()):
      print('ERROR: Could not open webcam (%d)' % self.devicenum)

    # Set to highest resolution!
    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920);
    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080);
    # self.cap.set(3, 1920)
    # self.cap.set(4, 1080)
    self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 0) # turn the autofocus off

    # Set the focus distance (multiples of 5).
    # Larger numbers focus on things closer up.
    self.cap.set(28, 10)

  def CaptureOcam(self):
    self.cap.release()
    cap = cv2.VideoCapture(self.devicenum)
    if (not self.cap.isOpened):
      print('Could not open ocam')
      return None

    ret, frame = cap.read()
    cap.release()
    return frame

  def Capture(self):
    # for i in range(4):
      # self.cap.grab()
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
