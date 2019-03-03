import cv2

from preprocess import *
from ocr import *
from camera_manager import *
from text_matching import *
from send_email import *

EMAIL_BODY = """\
  Your mail was just dropped off! Come pick it up when you get a chance."""

def Main():
  #============== SETUP ===============#
  cm = CameraManager(1)
  cv2.namedWindow('stream', cv2.WINDOW_NORMAL)
  cv2.namedWindow('crops', cv2.WINDOW_NORMAL)
  cv2.namedWindow('debug', cv2.WINDOW_NORMAL)

  #============== TRIGGER ==============#
  def Trigger():
    """
    This should be called every time mail is in the camera view.
    """
    img = cm.Capture()

    # Display the resulting frame
    # cv2.imshow('raw', img)
    # print('Press ENTER to continue')
    # cv2.waitKey(0)

    # Preprocess and get text.
    all_text = []
    roi = PreprocessImage(img)
    
    for r in roi:
      text = DetectText(r)
      all_text.append(text)      
      # cv2.imshow('crops', r)
      # cv2.waitKey(0)

    print('\n========= DETECTED TEXT =========')
    print(all_text)
    print('\n')

    # print('Press ENTER to continue')
    # cv2.waitKey(0)

    ## DO THE TEXT MATCHING HERE
    found_match = False

    # Send email if match found.
    if found_match:
      print('Match found! Sending them an email.')
      email = 'milokhl@gmail.com'
      SendEmail(email, EMAIL_BODY)    

  #=========== MAIN LOOP ============#
  while(True):
    img = cm.Capture()
    cv2.imshow('stream', img)

    # Press Q to quit.
    keycode = cv2.waitKey(5) & 0xFF
    if keycode == ord('q'):
      break

    # ENTER KEY TRIGGERS
    elif keycode == 13:
      print('ENTER PRESSED!')
      Trigger()

  cm.Shutdown()
  cv2.destroyAllWindows()

if __name__ == '__main__':
  Main()

# Test()
