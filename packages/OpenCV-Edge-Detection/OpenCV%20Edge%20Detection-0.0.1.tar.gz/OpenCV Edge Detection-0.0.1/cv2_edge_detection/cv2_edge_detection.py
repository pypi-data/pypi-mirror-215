# import the opencv library
import cv2
from edge_detection import *
import matplotlib.pyplot as plt
def run():
    # define a video capture object
    vid = cv2.VideoCapture(0)
      
    while(True):
          
        # Capture the video frame
        # by frame
        ret, frame = vid.read()
        frame=cv2.resize(frame,(1280,720))
        # Display the resulting frame
        cv2.imshow('frame2', frame)
        cv2.imshow('frame',convolve2D(frame,[[-1, -1, -1], [0, 0, 0], [1, 1, 1]]))
        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
      
    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()
