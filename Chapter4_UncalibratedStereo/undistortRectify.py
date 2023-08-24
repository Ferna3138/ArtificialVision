import cv2

# Camera parameters to undistort and rectify images
cvFile = cv2.FileStorage()
cvFile.open('stereoMap.xml', cv2.FileStorage_READ)

stereoMapLeft_x = cvFile.getNode('stereoMapLeft_x').mat()
stereoMapLeft_y = cvFile.getNode('stereoMapLeft_y').mat()
stereoMapRight_x = cvFile.getNode('stereoMapRight_x').mat()
stereoMapRight_y = cvFile.getNode('stereoMapRight_y').mat()

def undistortRectify(frameR, frameL):
    undistortedLeft= cv2.remap(frameL, stereoMapLeft_x, stereoMapLeft_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
    undistortedRight= cv2.remap(frameR, stereoMapRight_x, stereoMapRight_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)

    return undistortedRight, undistortedLeft