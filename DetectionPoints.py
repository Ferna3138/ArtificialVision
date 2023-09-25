#Face and landmarks detector

import cv2
import mediapipe as mp
import numpy as np
import math

lk_params = dict(winSize=(101, 101), maxLevel=15, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 20, 0.001))
def constrainPoint(point, width, height):
  point = (min(max(point[0], 0), width - 1), min(max(point[1], 0), height - 1))
  return point

class FaceDetector:
    def __init__(self):
        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(True, 1, True, 0.2, 0.5)
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=1, circle_radius=1, color=(200, 200, 0))

        self.stream_started = False

    def stabilizeVideoStream(self, frame, landmarks):
        img2Gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if not self.stream_started:
            self.points2Prev = np.array(landmarks, np.float32)
            self.img2GrayPrev = np.copy(img2Gray)
            self.stream_started = True

        points2Next, status, err = cv2.calcOpticalFlowPyrLK(self.img2GrayPrev, img2Gray, self.points2Prev, np.array(landmarks, np.float32), **lk_params)
        for k in range(0, len(landmarks)):
            d = cv2.norm(np.array(landmarks[k]) - points2Next[k])
            alpha = math.exp(-d * d / 50)
            landmarks[k] = (1 - alpha) * np.array(landmarks[k]) + alpha * points2Next[k]
            landmarks[k] = constrainPoint(landmarks[k], frame.shape[1], frame.shape[0])
            landmarks[k] = (int(landmarks[k][0]), int(landmarks[k][1]))

        self.points2Prev = np.array(landmarks, np.float32)
        self.img2GrayPrev = img2Gray



    def drawLandmarks(self, img, landmarks):
        out = np.copy(img)

        self.mpDraw.draw_landmarks(out, landmarks, self.mpFaceMesh.FACEMESH_TESSELATION, self.drawSpec, self.drawSpec)
        self.mpDraw.draw_landmarks(out, landmarks, self.mpFaceMesh.FACEMESH_CONTOURS, self.drawSpec, self.drawSpec)
        #self.mpDraw.draw_landmarks(out, landmarks, self.mpFaceMesh.FACEMESH_IRISES, self.drawSpec, self.drawSpec)

        return out


    # Process facemesh and find landmarks
    def findFaceLandmarks(self, img, draw=False):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.faceMesh.process(imgRGB)

        selectedKeypointIndices = [127, 93, 58, 136, 150, 149, 176, 148, 152, 377, 400, 378, 379, 365, 288, 323, 356,
                                     70, 63, 105, 66, 55,
                                     285, 296, 334, 293, 300, 168, 6, 195, 4, 64, 60, 94, 290, 439, 33, 160, 158, 173,
                                     153, 144, 398, 385,
                                     387, 466, 373, 380, 61, 40, 39, 0, 269, 270, 291, 321, 405, 17, 181, 91, 78, 81,
                                     13, 311, 306, 402, 14,
                                     178, 162, 54, 67, 10, 297, 284, 389]

        if not results.multi_face_landmarks:
            print('No face detected')
            return [], None, None

        landmarks = []
        height, width = img.shape[:-1]

        if results.multi_face_landmarks:
            faceLandmarks = results.multi_face_landmarks[0]
            if draw:
                self.drawLandmarks(img, faceLandmarks)

            values = np.array(faceLandmarks.landmark)
            faceKeypoints = np.zeros((len(values), 2))

            for idx, value in enumerate(values):
                faceKeypoints[idx][0] = value.x
                faceKeypoints[idx][1] = value.y

            faceKeypoints = faceKeypoints * (width, height)
            faceKeypoints = faceKeypoints.astype('int')

            for i in selectedKeypointIndices:
                landmarks.append(faceKeypoints[i])

        return landmarks, img, faceLandmarks

    def loadTargetImg(self, img_path):
        img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        img = cv2.resize(img, (480,640), interpolation=cv2.INTER_AREA)
        b, g, r, alpha = cv2.split(img)
        img = cv2.merge((b, g, r))
        return img, alpha