import imutils
import cv2
import numpy as np
import argparse
from skimage import exposure


ap = argparse.ArgumentParser()
ap.add_argument("-q", "--query", required = True, help = "path to the query image")
args = vars(ap.parse_args())


image = cv2.imread(args["query"])
# smaller image = faster processing but too small means you lose out on key features
ratio = image.shape[0] / 300.0
original = image.copy()
original = imutils.rotate(original, 90)
image = imutils.resize(image, height = 300)
image = imutils.rotate(image, 90)

# convert the image to gray scale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# blur the image using bilateral filter.
# this fn has the nice property of removing noise from the image preserving the edges 

gray = cv2.bilateralFilter(gray, 11, 17, 17)

# cv2.imshow("blurred image", gray)
# cv2.waitKey(0)


#finally we apply Canny edge detection
# 2nd arg - lower bound
# 3rd arg - upper bound
edged = cv2.Canny(gray, 30, 200)

# cv2.imshow("edges", edged)
# cv2.waitKey(0)

# contour essentially means the outline or silhouette of an object. 
# An image can have several contours

# we are passing the copy here because the findContours function destroys(manipulates) the image.
# if we want to use the original image again, we must be sure to pass only a copy to findContours 
# cv2.RETR_TREE = compute the hierarchy(relationship) between contours
# cv2.RETR_LIST could also have been used.
# cv2.CHAIN_APPROX_SIMPLE = copmress and resize the contour to save space.
# cnts is a List of contours OpenCV has found in our image.
(edged_copy, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# sort the contours and save only the 10 biggest contours
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]

# our actual pokemon contour.
screenCnt = None


# loop through the cnts list to find the pokemon contour (outline/silhouette)
for c in cnts:
	# approximate the contour
	peri = cv2.arcLength(c, True)

	# second argument is approximation precision.
	# over here it is 2% of the perimeter. (very IMPORTANT PARAMETER, have to play around to find out exact value)
	# 
	approx = cv2.approxPolyDP(c, 0.02*peri, True)


	if len(approx) is 4: 
		screenCnt = approx
		break


# first argument obviously is the image we want to draw the contour on
# second argument is the contour dimensions
# third argument - not sure
# fourth argument is the color (BLUE, GREEN, RED) format
# fifth argument is the thickness
cv2.drawContours(image, [screenCnt], 0, (128, 0, 0), 3)
cv2.imshow("Game boy screen", image)
cv2.waitKey(0)


# step to find all the four points of our contour, the top-left, top-right, bottom-right, bottom-left
pts = screenCnt.reshape(4,2)
print(pts)


# initialize a 4x2 floating point valued array
rect = np.zeros((4,2), dtype = "float32")
print(rect)

# axis = 0 gives the output sum of all the columns, here since we have 2 columns, we will get 2 columns in output
# axis = 1 gives the output sum of all the rows, here since we have 4 rows, we will get values in output
s = pts.sum(axis = 1)
print(s)

# top left has the smallest sum
rect[0] = pts[np.argmin(s)]
# bottom right has the largest sum
rect[2] = pts[np.argmax(s)]

diff = np.diff(pts, axis = 1)

# top right has the smallest difference
rect[1] = pts[np.argmin(diff)]
# bottom left has the largest difference
rect[3] = pts[np.argmax(diff)]

# multiply the ratio so that we dont lose the original game boy image while cropping and resizing.
rect *= ratio

(tl, tr, br, bl) = rect

# calculating the x coordinates and the y coordinates of the width and the height of the resized/cropped image
widthA = np.sqrt( ((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2) )
widthB = np.sqrt( ((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2) )


heightA = np.sqrt( ((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2) )
heightB = np.sqrt( ((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2) )


maxWidth = max(int(widthA), int(widthB))
maxHeight = max(int(heightA), int(heightB))

# From here, we are gonna construct our destination point which will be used to map our gameboy screen
# this is where the perspective transformation happens.

dst = np.array([ [0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1] ], dtype = "float32")


# calculate the perspective transformation matrix and warp the perspective to grab the image.
# 1st argument = original image.
# 2nd argument = four points we specified for our output image, here the tl , tr, br, bl order matters, that's why we created dst
M = cv2.getPerspectiveTransform(rect, dst)

# 1st argument = the original image
# 2nd argument = the transformation matrix
# 3rd argument = the new height and width
warp = cv2.warpPerspective(original, M , (maxWidth, maxHeight))

cv2.imshow("warped image", warp)
cv2.waitKey(0)

warp = cv2.cvtColor(warp, cv2.COLOR_BGR2GRAY)

# all the pixels that fall into this range have their intensity rescaled
warp = exposure.rescale_intensity(warp, out_range = (0, 255))


(h, w) = warp.shape

# done by trial and error only
(dX, dY) = (int(w * 0.4), int(h * 0.45))
crop = warp[10:dY, w - dX:w - 10]


cv2.imwrite("cropped.png", crop)


cv2.imshow("image", image)
cv2.imshow("edge", edged)
cv2.imshow("warp", imutils.resize(warp, height = 300))
cv2.imshow("crop", imutils.resize(crop, height = 300))
cv2.waitKey(0)




































