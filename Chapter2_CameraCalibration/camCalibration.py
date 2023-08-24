import numpy as np
import cv2 as cv
import glob
import pickle


# Set chessboard borders - Object points and image points
chessboardSize = (7,7)  # X number of corners & Y number of corners
frameSize = (1620,1080)

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points such as (0,0,0), (1,0,0), (2,0,0)
objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

sizeChessboardSquares_mm = 25
objp = objp * sizeChessboardSquares_mm

objPoints = [] # 3d point in real world space from the actual chessboard
imgPoints = [] # 2d points in image plane

images = glob.glob('CalibrationImages\SonyA7IV Sigma art 24mm\*.JPG')

for image in images:
    #print(image)
    img = cv.imread(image)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, chessboardSize, None)

    # If found, add object points and image points
    if ret == True:
        objPoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        imgPoints.append(corners)

        # Draw and display corners
        cv.drawChessboardCorners(img, chessboardSize, corners2, ret)
        cv.imshow('img', img)
        cv.waitKey(1000)

cv.destroyAllWindows()

# Calibration
ret, cameraMatrix, dist, rotationVecs, translationVecs = cv.calibrateCamera(objPoints, imgPoints, frameSize, None, None)

# Save the camera calibration result
pickle.dump((cameraMatrix, dist), open("calibration.pkl", "wb"))
pickle.dump(cameraMatrix, open("cameraMatrix.pkl", "wb"))
pickle.dump(dist, open("dist.pkl", "wb"))


# Undistort
img = cv.imread('CalibrationImages/SonyA7IV Sigma art 24mm/DSC01457.jpg')
h,  w = img.shape[:2]
newCameraMatrix, regionOfInterest = cv.getOptimalNewCameraMatrix(cameraMatrix, dist, (w, h), 1, (w, h))


#dst = cv.undistort(img, cameraMatrix, dist, None, newCameraMatrix)
# Crop image
#x, y, w, h = roi
#dst = dst[y:y+h, x:x+w]
#.imwrite('caliResult1.png', dst)


# Undistort with Remapping
mapX, mapY = cv.initUndistortRectifyMap(cameraMatrix, dist, None, newCameraMatrix, (w, h), 5)
out = cv.remap(img, mapX, mapY, cv.INTER_LINEAR)

# Crop image
x, y, w, h = regionOfInterest
out = out[y:y + h, x:x + w]
cv.imwrite('CalibrationImages/Results/DSC01457_Calibrated.png', out)


# Reprojection Error
meanError = 0

for i in range(len(objPoints)):
    imgPoints2, _ = cv.projectPoints(objPoints[i], rotationVecs[i], translationVecs[i], cameraMatrix, dist)
    error = cv.norm(imgPoints[i], imgPoints2, cv.NORM_L2) / len(imgPoints2)
    meanError += error

print("Error: {}".format(meanError / len(objPoints)))
print("Camera Matrix: \n", cameraMatrix)
print("Rotation vecs: \n", rotationVecs)
print("Translation vecs: \n", translationVecs)
