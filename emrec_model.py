from paz.pipelines import MiniXceptionFER
import cv2
import numpy as np
import os

path_to_video = os.path.join(
    '/home/danil/Downloads', 
    'tomp3.cc - Zoom Class Meeting Downing Sociology 220 10222020_1080p (online-video-cutter.com).mp4'
)

cap = cv2.VideoCapture(path_to_video)
 
# Check if video opened successfully
if (cap.isOpened() == False): 
  print("Error opening video stream or file")

# outputs probabilities for {“angry”, “disgust”, “fear”, “happy”, “sad”, “surprise”, “neutral”}
# preserving order
classifier = MiniXceptionFER()

recognised_frames = []
# Read until video is completed
while(cap.isOpened()):
  
  # ret -- flag, indicating, whether the file returned frame
  # frame -- video frame (image) itself
  ret: bool
  frame: np.array
  ret, frame = cap.read()
  if ret == True:

    cv2.imshow('Frame', frame)

    inference = classifier(frame)
    inference['timestamp'] = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
    print(inference)
 
    # Press q on keyboard to exit
    if (cv2.waitKey(25) & 0xFF) == ord('q'):
      break

  else: 
    break
 
# When everything done, release the video capture object
cap.release()
 
# Closes all the frames
cv2.destroyAllWindows()