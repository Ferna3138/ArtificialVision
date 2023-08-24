import sys
import cv2
import numpy as np
import time

def findDepth(circleRight, circleLeft, frameRight, frameLeft, baseline, alpha):

    # Focal length f from mm tp pixel
    heightRight, widthRight, depthRight = frameRight.shape
    heightLeft, widthLeft, depthLeft = frameLeft.shape

    #if widthRight == widthLeft:
    fPixel = (widthRight * 0.5) / np.tan(alpha * 0.5 * np.pi / 180) #Focal length in pixels
    #else:
     # print('Pixel width of each camera do not match')

    # Due to the lack of a proper 2 camera equal frame size setup, this if statement is commented
    # To be enabled in case of a proper equally sized stereo framing

    xRight = circleRight[0]
    xLeft = circleLeft[0]

    disparity = xLeft - xRight

    # Depth in cm
    zDepth = (baseline * fPixel) / disparity

    return abs(zDepth)