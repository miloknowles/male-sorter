import cv2

from preprocess import *
from ocr import *
from camera_manager import *
from text_matching import *
from send_email import *
from sorter import *

EMAIL_BODY = """\
  Your mail was just dropped off! Come pick it up when you get a chance."""

DATABASE = {
  "Victor Pontis":"iperper@mit.edu",
  "Christopher Puchi": "iperper@mit.edu",
  "Enes Goktas": "iperper@mit.edu",
  "Arash Kani":"iperper@mit.edu",
  "Diana Martin": "iperper@mit.edu",
  "Rob Wheeler": "iperper@mit.edu",
  "Jacob Jurewicz": "iperper@mit.edu" ,
  "Mark Halsey": "iperper@mit.edu",
  "Lizi Yuan": "iperper@mit.edu",
  "Delian Asparouhov": "mknowles@mit.edu"
}

FULL_NAMES = list(DATABASE.keys())

def Main():
  #============== SETUP ===============#
  cm = CameraManager(1)
  cv2.namedWindow('stream', cv2.WINDOW_NORMAL)
  cv2.namedWindow('crops', cv2.WINDOW_NORMAL)
  cv2.namedWindow('debug', cv2.WINDOW_NORMAL)

  COM = '/dev/ttyACM0'
  baudRate = 9600
  
  ser = serial.Serial(COM, baudRate)
  time.sleep(5)

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
    joined_text = ' '.join(all_text)
    joined_text.replace('\t', '')
    match_score, match_name = best_matches(joined_text, FULL_NAMES, 0.9)
    print('========== DATABASE MATCHING ==========')
    print('Name: %s Score: %s' % (str(match_name), str(match_score)))

    # Send email if match_scorech found.
    # if match_score is not None:
      # email = DATABASE[match_name]
    email = "milokhl@gmail.com"
    print('Match found! Sending %s an email.' % (email))
    SendEmail(email, EMAIL_BODY)  

    flip_mail(ser)
    time.sleep(2)
    drop_mail(ser)

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
  ser.close()

if __name__ == '__main__':
  Main()

# Test()
