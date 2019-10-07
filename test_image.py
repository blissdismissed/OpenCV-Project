# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
rawCapture = PiRGBArray(camera)

camera.start_preview()
# allow the camera to warmup
time.sleep(5)

# grab an image from the camera
#camera.capture(rawCapture, format="bgr")
camera.capture('/home/pi/Desktop/image.jpg')
#image = rawCapture.array

camera.stop_preview()

# display the image on screen and wait for a keypress
#cv2.imshow("Image", image)
#cv2.waitKey(1000)