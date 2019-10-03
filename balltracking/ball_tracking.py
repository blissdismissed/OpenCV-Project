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
    vs = VideoStream(src=0).start()
    
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
    
    # find contours in mask, init center
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None
    
    # only process if at least one contour is found
    if len(cnts) > 0:
        # find largest contour in mask
        # compute min enclosing circle and centroid
        c = max(cnts, key=cv2.contourArea)
        ((x,y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        
        # only proceed if radius meets a min size
        if radius > 10:
            # draw circle and centroid on frame
            # update list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            
    # update the points queue
    pts.appendleft(center)
    
    # loop over set of tracked points
    for i in range(1, len(pts)):
        # if either are None, ignore
        if pts[i-1] is None or pts[i] is None:
            continue
        
        # otherwise draw it
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i-1], pts[i], (0, 0, 255), thickness)
        
    # show frame to screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    
    # if q is pressed stop the loop
    if key == ord("q"):
        break

# if not using a video file, stop the camera stream
if not args.get("video", False):
    vs.stop()

# otherwise, release the camera
else:
    vs.release()
    
# close all windows
cv2.destroyAllWindows()

    
    