import cv2
import time
from mycroft.util import LOG
import os

def take_photo(img_queue):
    '''
    Do taking photo
    '''
    LOGSTR = '********************====================########## '
    LOG.info(LOGSTR + 'take photo process start')
    cap = cv2.VideoCapture(0)
    img_name = 'test.jpg'
    img_path = '/home/ai-user/mycroft-core/skills/voiceassistant-skill/' + img_name # Remember to update path to image

    #<-- Take photo in specific time duration -->
    cout = 0
    while True:
        ret, frame = cap.read()
        cv2.waitKey(1)
        cv2.imshow('capture', frame)
        cout += 1 
        if cout == 50:
            img_queue.put(img_path)
            cv2.imwrite(img_path, frame)
            break

    cap.release()
    cv2.destroyAllWindows()
    LOG.info(LOGSTR + 'take photo process end')
    os._exit(0)

