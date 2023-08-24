import cv2
import numpy as np

from Chapter3_SimpleStereo import HSV_filter as hsv, shapeRecognition as shape
import triangulation as tri

capRight = cv2.VideoCapture(0, cv2.CAP_DSHOW)
capLeft = cv2.VideoCapture(1, cv2.CAP_DSHOW)

frameRate = 25
Baseline = 15               #Distance between the cameras
focalLength = 24            #Camera lense's focal length
alpha = 84.1                #Camera field of view in the horisontal plane
                            #Sigma art 35mm = 63 degrees
                            #Sigma art 24mm = 84.1 degrees


count = -1

while(True):
    count += 1

    retRight, frameRight = capRight.read()
    retLeft, frameLeft = capLeft.read()

#Calibration
    if retRight==False or retLeft==False:
        break

    else:
        # HSV
        maskRight = hsv.add_HSV_filter(frameRight, 1)
        maskLeft = hsv.add_HSV_filter(frameLeft, 0)

        # Result after applying HSV filter mask
        resRight = cv2.bitwise_and(frameRight, frameRight, mask=maskRight)
        resLeft = cv2.bitwise_and(frameLeft, frameLeft, mask=maskLeft)

        # Shape recognition
        circlesRight = shape.findCircles(frameRight, maskRight)
        circlesLeft = shape.findCircles(frameLeft, maskLeft)

        # Calculating depth
        if np.all(circlesRight) == None or np.all(circlesLeft) == None:
            cv2.putText(frameRight, "TRACKING LOST", (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frameLeft, "TRACKING LOST", (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            #Triangulation file that defines the depth of the object
            depth = tri.findDepth(circlesRight, circlesLeft, frameRight, frameLeft, Baseline, alpha)

            cv2.putText(frameRight, "TRACKING", (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124, 252, 0), 2)
            cv2.putText(frameLeft, "TRACKING", (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124, 252, 0), 2)
            cv2.putText(frameRight, "Distance: " + str(round(depth, 3)), (200, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124, 252, 0), 2)
            cv2.putText(frameLeft, "Distance: " + str(round(depth, 3)), (200, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124, 252, 0), 2)
            print("Depth: ", depth)


        cv2.imshow("Frame Right", frameRight)
        cv2.imshow("Frame Left", frameLeft)
        cv2.imshow("Mask Right", maskRight)
        cv2.imshow("Mask Left", maskLeft)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

capRight.release()
capLeft.release()

cv2.destroyAllWindows()