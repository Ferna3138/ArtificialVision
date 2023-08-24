import cv2

# Function for stereo vision and depth estimation
from Chapter3_SimpleStereo import triangulation as tri
import undistortRectify

# Mediapipe for face detection
import mediapipe as mp
import time


mpFacedetector = mp.solutions.face_detection
mpDraw = mp.solutions.drawing_utils

# Stereo vision setup parameters
frameRate = 30
baseLine = 10
focalLength = 5
alpha = 65


capRight = cv2.VideoCapture(0, cv2.CAP_DSHOW)
capLeft = cv2.VideoCapture(2, cv2.CAP_DSHOW)


with mpFacedetector.FaceDetection(min_detection_confidence=0.7) as face_detection:
    while (capRight.isOpened() and capLeft.isOpened()):

        successRight, frameRight = capRight.read()
        successLeft, frameLeft = capLeft.read()

        # Calibration
        frameRight, frameLeft = undistortRectify.undistortRectify(frameRight, frameLeft)

        if not successRight or not successLeft:
            break
        else:
            start = time.time()

            # BGR to RGB Convert
            frameRight = cv2.cvtColor(frameRight, cv2.COLOR_BGR2RGB)
            frameLeft = cv2.cvtColor(frameLeft, cv2.COLOR_BGR2RGB)

            # Process the image and find faces
            resultsRight = face_detection.process(frameRight)
            resultsLeft = face_detection.process(frameLeft)

            # Convert the RGB image to BGR
            frameRight = cv2.cvtColor(frameRight, cv2.COLOR_RGB2BGR)
            frameLeft = cv2.cvtColor(frameLeft, cv2.COLOR_RGB2BGR)

            centreRight = 0
            centreLeft = 0

            # Detect both frames individually
            if resultsRight.detections:
                for id, detection in enumerate(resultsRight.detections):
                    mpDraw.draw_detection(frameRight, detection)
                    bBox = detection.location_data.relative_bounding_box

                    height, width, channels = frameRight.shape

                    boundBox = int(bBox.xmin * width), int(bBox.ymin * height), int(bBox.width * width), int(bBox.height * height)
                    centrePointRight = (boundBox[0] + boundBox[2] / 2, boundBox[1] + boundBox[3] / 2)

                    cv2.putText(frameRight, f'{int(detection.score[0] * 100)}%', (boundBox[0], boundBox[1] - 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)

            if resultsLeft.detections:
                for id, detection in enumerate(resultsLeft.detections):
                    mpDraw.draw_detection(frameLeft, detection)
                    bBox = detection.location_data.relative_bounding_box

                    height, width, channels = frameLeft.shape

                    boundBox = int(bBox.xmin * width), int(bBox.ymin * height), int(bBox.width * width), int(bBox.height * height)
                    centrePointLeft = (boundBox[0] + boundBox[2] / 2, boundBox[1] + boundBox[3] / 2)

                    cv2.putText(frameLeft, f'{int(detection.score[0] * 100)}%', (boundBox[0], boundBox[1] - 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)


            if not resultsRight.detections or not resultsLeft.detections:
                cv2.putText(frameRight, "TRACKING LOST", (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(frameLeft, "TRACKING LOST", (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                depth = tri.findDepth(centrePointRight, centrePointLeft, frameRight, frameLeft, baseLine, alpha)

                cv2.putText(frameRight, "Distance: " + str(round(depth, 2)), (50, 50), cv2.QT_FONT_NORMAL, 1.2,
                            (0, 255, 0), 3)
                cv2.putText(frameLeft, "Distance: " + str(round(depth, 2)), (50, 50), cv2.QT_FONT_NORMAL, 1.2,
                            (0, 255, 0), 3)

                print("Depth: ", str(round(depth, 1)))

            end = time.time()
            totalTime = end - start

            fps = 1 / totalTime
            # print("FPS: ", fps)

            cv2.putText(frameRight, f'FPS: {int(fps)}', (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
            cv2.putText(frameLeft, f'FPS: {int(fps)}', (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)

            cv2.imshow("Frame Right", frameRight)
            cv2.imshow("Frame Left", frameLeft)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

capRight.release()
capLeft.release()

cv2.destroyAllWindows()