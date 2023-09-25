import cv2
import numpy as np
from DetectionPoints import FaceDetector
from MaskGenerate import MaskGenerator

cap = cv2.VideoCapture(0)
detector = FaceDetector()
maskGenerator = MaskGenerator()

def showImages(actual, target, output1, output2):
    imgCurrent = np.copy(actual)
    imgTarget = np.copy(target)

    imgOut1 = np.copy(output1)
    imgOut2 = np.copy(output2)

    # Resize 640x480 -> 360x480
    imgCurrent = imgCurrent[:, 140:500]
    imgOut1 = imgOut1[:, 140:500]

    # Resize 480x640 -> 360x480
    imgTarget = cv2.resize(imgTarget, (360, 480), interpolation=cv2.INTER_AREA)
    imgOut2 = cv2.resize(imgOut2, (360, 480), interpolation=cv2.INTER_AREA)

    h1 = np.concatenate((imgCurrent, imgTarget, imgOut1, imgOut2), axis=1)

    cv2.imshow('Face Mask', h1)

# Target
targetImage, targetAlpha = detector.loadTargetImg("images/frodo.png")

targetLandmarks, _, targetFaceLandmarks = detector.findFaceLandmarks(targetImage)
targetImageOut = detector.drawLandmarks(targetImage, targetFaceLandmarks)

maskGenerator.calculateTargetInfo(targetImage, targetAlpha, targetLandmarks)

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)

    landmarks, image, faceLandmarks = detector.findFaceLandmarks(frame)
    if len(landmarks) == 0:
        continue

    detector.stabilizeVideoStream(frame, landmarks)

    output = maskGenerator.applyTargetMask(frame, landmarks)
    output2 = maskGenerator.applyTargetMaskToTarget(landmarks)

    imageOut = detector.drawLandmarks(image, faceLandmarks)
    showImages(imageOut, targetImageOut, output, output2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break