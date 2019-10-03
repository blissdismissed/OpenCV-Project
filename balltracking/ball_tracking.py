from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

# construct arg parse and parse arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,help="max buffer size")
args = vars(ap.parse_args())

# define boundaries of ball in HSV color space
# (hue,saturation,value) --> use range detector in imutils library
# init the list of tracked points
greenLower = (29,86,6)
greenUpper = (64,255,255)
pts = deque(maxlen=args["buffer"])

# if no videopath given, use camera
if not args.get("video", False):
    vs = VideoStream(src=0.start())
    
# otherwise get the reference to the video file
else:
    vs = cv2.VideoCapture(args["video"])

# allow time for loading/warmup
time.sleep(2.0)

# watching the object
while True:
    # grab the current frame
    frame = vs.read()
    
    # handle frame from videocapture or videostream
    frame = frame[1] if args.get("video", False) else frame
    
    # if we are viewing a video and did not grab a frame
    # maybe video is finished
    if frame is None:
        break
    
    # resize frame, blur, convert to HSV color space
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    # construct mask for color "green"
    # do some erosions and dilations to remove small blobs
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)