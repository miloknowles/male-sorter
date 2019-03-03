from camera_manager import *

def TestNormal():
  cm = CameraManager(1)
  cm.Stream()
  cm.Shutdown()

def TestOcam():
  cm = CameraManager(1)
  frame = cm.CaptureOcam()
  cv2.imshow('ocam', frame)
  cv2.waitKey(0)

def TestSetFocus():
  cm = CameraManager(1)
  
  for depth in [0, 5, 10, 40, 100, 255]:
    cm.cap.set(28, int(depth))

    frame = cm.Capture()
    cv2.imshow('frame', frame)
    cv2.waitKey(0)  

# TestOcam()
# TestSetFocus()
TestNormal()
