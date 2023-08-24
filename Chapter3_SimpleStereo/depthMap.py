import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

leftImage = cv.imread('depthMap/DepthMap_Test1_Left.png', cv.IMREAD_GRAYSCALE)
rightImage = cv.imread('depthMap/DepthMap_Test1_Right.png', cv.IMREAD_GRAYSCALE)

stereo = cv.StereoBM_create(numDisparities=0, blockSize=19)
depth=stereo.compute(leftImage,rightImage)

cv.imshow('Left', leftImage)
cv.imshow('Right', rightImage)

plt.imshow(depth)
plt.axis('off')
plt.savefig('depthMap/Export/DepthMap_Test1.png')