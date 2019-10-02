# import the necessary packages
from __future__ import print_function
from pyimagesearch.notifications import TwilioNotifer
from pyimagesearch.utils import Conf
from imutils.video import VideoStream
from imutils.io import TempFile
from datetime import datetime
from datetime import data
import  numpy as np
import argparse
import imutils
import signal
import time
import cv2
import sys

# function to handle keyboard interrupt
def signal_handler(sig, frame):
    print("[INFO] You pressed 'ctrl + c'! Closing refrigerator monitor" \
        " application...")
    sys.exit(0)

# construct the argument parser and parse the args
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True, help="Path to the input configuration file")
args = vars(ap.parse_args())

