import cv2

capRight = cv2.VideoCapture(0)
capLeft = cv2.VideoCapture(2)

count = 0

retRight, frameRight = capRight.read()
print('Resolution Right: ' + str(frameRight.shape[0]) + ' x ' + str(frameRight.shape[1]))

retLeft, frameLeft = capRight.read()
print('Resolution Left: ' + str(frameLeft.shape[0]) + ' x ' + str(frameLeft.shape[1]))

while capRight.isOpened():
    successRight, imgRight = capRight.read()
    successLeft, imgLeft = capLeft.read()

    if cv2.waitKey(1) == ord('q'):
        break
    elif cv2.waitKey(1) == ord('s'): # Press S to save images
        cv2.imwrite('../StereoCalibration/RightCamera/Right_Calibration_' + str(count) + '.png', imgRight)
        cv2.imwrite('../StereoCalibration/LeftCamera/Left_Calibration_' + str(count) + '.png', imgLeft)
        print("Saved!")
        count += 1

    cv2.imshow('Right', imgRight)
    cv2.imshow('Left', imgLeft)

capRight.release()
capLeft.release()
cv2.destroyAllWindows()