import numpy as np
import cv2


def detect(image):

	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx = 1, dy = 0, ksize = -1)
	gradY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx = 0, dy = 1, ksize = -1)

	# we subtract the y-gradient from the x-gradient
	# why? to be left with images that have high vertical gradient and low horizontal gradient, basically the barcoded region
	gradient = cv2.subtract(gradX, gradY)
	gradient = cv2.convertScaleAbs(gradient)

	# applying blur to smooth out high frequency noise using a 9x9 kernel
	blurred = cv2.blur(gradient, (9, 9))

	(_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)

	# after doing all this, there will be gaps in the barcode, for which we
	# apply morphological open and then apply a series of erosions and dilations

	# construct a rectangular kernel
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
	# we are doing MORPH_CLOSE than morph open because we want a filler rectangle to be detected by findContours I guess.
	closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

	# an erosion will erode the white pixels in the image, thus removing the small blobs/false positives
	closed = cv2.erode(closed, None, iterations = 4)
	# dilate will grow the remaining white regions bigger
	closed = cv2.dilate(closed, None, iterations = 4)


	(_, cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	if len(cnts) == 0:
		return None

	c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]

	# compute the minimum bounding box for the largest contour
	rect = cv2.minAreaRect(c)
	box = np.int0(cv2.boxPoints(rect))

	return box