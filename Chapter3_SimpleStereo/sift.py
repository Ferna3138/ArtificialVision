import cv2

sift = cv2.SIFT_create()

# Feature matching
bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)


img1 = cv2.imread('L.jpg')
img2 = cv2.imread('R.jpg')

img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

keypointsImg1, descriptorsImg1 = sift.detectAndCompute(img1, None)
keypointsImg2, descriptorsImg2 = sift.detectAndCompute(img2, None)

matches = bf.match(descriptorsImg1, descriptorsImg2)
matches = sorted(matches, key = lambda x:x.distance)

img3 = cv2.drawMatches(img1, keypointsImg1, img2, keypointsImg2, matches[:50], img2, flags=2)

cv2.imshow('SIFT', img3)

cv2.waitKey(0)