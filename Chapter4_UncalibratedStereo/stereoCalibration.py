import numpy as np
import cv2 as cv
import glob

chessboardSize = (11,7)
frameSize = (640,480)

# Square size in centimeters
squareSizeCM = 2.1

# Chessboard size in centimeters
chessboardWidthCM = 25.75
chessboardHeightCM = 17.1

# Convert square size and chessboard size to meters
squareSizeM = squareSizeCM / 100.0
chessboardWidthM = chessboardWidthCM / 100.0
chessboardHeightM = chessboardHeightCM / 100.0

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0)
objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

objp = objp * 21

# 3d point in real world space
objPoints = []

# 2d points in image plane
imgPointsLeft = []
imgPointsRight = []


imagesLeft = glob.glob('../StereoCalibration/LeftCamera/*.png')
imagesRight = glob.glob('../StereoCalibration/RightCamera/*.png')

for imagesLeft, imagesRight in zip(imagesLeft, imagesRight):
    imgL = cv.imread(imagesLeft)
    imgR = cv.imread(imagesRight)
    grayLeft = cv.cvtColor(imgL, cv.COLOR_BGR2GRAY)
    grayRight = cv.cvtColor(imgR, cv.COLOR_BGR2GRAY)

    # Find the chess board corners
    retL, cornersLeft = cv.findChessboardCorners(grayLeft, chessboardSize, None)
    retR, cornersRight = cv.findChessboardCorners(grayRight, chessboardSize, None)

    if retL and retR == True:
        objPoints.append(objp)

        # Corner scan accuracy improvement
        cornersLeft = cv.cornerSubPix(grayLeft, cornersLeft, (11, 11), (-1, -1), criteria)
        imgPointsLeft.append(cornersLeft)

        cornersRight = cv.cornerSubPix(grayRight, cornersRight, (11, 11), (-1, -1), criteria)
        imgPointsRight.append(cornersRight)

        # Display the corners
        cv.drawChessboardCorners(imgL, chessboardSize, cornersLeft, retL)
        cv.imshow('img left', imgL)
        cv.drawChessboardCorners(imgR, chessboardSize, cornersRight, retR)
        cv.imshow('img right', imgR)
        cv.waitKey(1000)


cv.destroyAllWindows()



# Calibration of both cameras
# Left
retL, cameraMatrixLeft, distortionLeft, rotationVecsLeft, translationVecsLeft = cv.calibrateCamera(objPoints, imgPointsLeft, frameSize, None, None)
heightLeft, widthLeft, channelsLeft = imgL.shape

newCameraMatrixLeft, roiLeft = cv.getOptimalNewCameraMatrix(cameraMatrixLeft, distortionLeft, (widthLeft, heightLeft), 1, (widthLeft, heightLeft))

#Right
retR, cameraMatrixRight, distortionRight, rotationVecsRight, translationVecsRight = cv.calibrateCamera(objPoints, imgPointsRight, frameSize, None, None)
heightRight, widthRight, channelsRight = imgR.shape

newCameraMatrixRight, roiRight = cv.getOptimalNewCameraMatrix(cameraMatrixRight, distortionRight, (widthRight, heightRight), 1, (widthRight, heightRight))


# Stereo Calibration
flags = 0
flags |= cv.CALIB_FIX_INTRINSIC

stereoCriteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# This step is performed to transformation between the two cameras and calculate Essential and Fundamental matrix
retStereo, newCameraMatrixLeft, distortionLeft, newCameraMatrixRight, distortionRight, rotation, translation, essentialMatrix, fundamentalMatrix = cv.stereoCalibrate(objPoints, imgPointsLeft, imgPointsRight, newCameraMatrixLeft, distortionLeft, newCameraMatrixRight, distortionRight, grayLeft.shape[::-1], stereoCriteria, flags)

print(newCameraMatrixLeft)
print(newCameraMatrixRight)

# Rectification
rectifyScale = 1
rectLeft, rectRight, projMatrixLeft, projMatrixRight, QMatrix, roiLeft, roiRight= cv.stereoRectify(newCameraMatrixLeft, distortionLeft, newCameraMatrixRight, distortionRight, grayLeft.shape[::-1], rotation, translation, rectifyScale, (0, 0))

stereoMapLeft = cv.initUndistortRectifyMap(newCameraMatrixLeft, distortionLeft, rectLeft, projMatrixLeft, grayLeft.shape[::-1], cv.CV_16SC2)
stereoMapRight = cv.initUndistortRectifyMap(newCameraMatrixRight, distortionRight, rectRight, projMatrixRight, grayRight.shape[::-1], cv.CV_16SC2)

print("Saving parameters")
cvFile = cv.FileStorage('stereoMap.xml', cv.FILE_STORAGE_WRITE)

cvFile.write('stereoMapLeft_x', stereoMapLeft[0])
cvFile.write('stereoMapLeft_y', stereoMapLeft[1])
cvFile.write('stereoMapRight_x', stereoMapRight[0])
cvFile.write('stereoMapRight_y', stereoMapRight[1])

cvFile.release()
