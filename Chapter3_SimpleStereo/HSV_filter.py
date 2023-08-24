import sys
import cv2
import numpy as np
import time

def add_HSV_filter(frame, camera):
    blur = cv2.GaussianBlur(frame,(5,5),0)

    # RGB to HSV Conversion
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    lowerBoundRight = np.array([60, 110, 50])
    upperBoundRight = np.array([255, 255, 255])
    lowerBoundLeft = np.array([60, 110, 50])
    upperBoundLeft = np.array([255, 255, 255])

	# HSV-filter mask
	#mask = cv2.inRange(hsv, lowerBoundLeft, upperBoundLeft)

    if(camera == 1):
        mask = cv2.inRange(hsv, lowerBoundRight, upperBoundRight)
    else:
        mask = cv2.inRange(hsv, lowerBoundLeft, upperBoundLeft)

    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    return mask