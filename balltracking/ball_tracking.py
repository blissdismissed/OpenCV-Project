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