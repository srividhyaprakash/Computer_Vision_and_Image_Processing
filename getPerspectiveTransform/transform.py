import numpy as np
import cv2

# pts = list of four (x, y) coordinates in a specified order
# the order is top-left, top-right, bottom-left, bottom-right

def order_points(pts):

	rect = np.zeros((4, 2), dtype = "float32")

	# The top-left will have the min sum
	# the bottom-right will have the max sum 
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]

	# the top-right will have the min difference
	# the bottom-left will have the max difference
	diff = np.diff(pts, axis = 1)

	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]

	return rect


def four_point_transform(image, pts):
	rect = order_points(pts)

	(tl, tr, br, bl) = rect


	# distance between two points = ( (x2 - x1)^2 + (y2 - y1)^2 )^0.5
	widthA = np.sqrt( ((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2) )
	widthB = np.sqrt( ((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2) )

	maxWidth = max(int(widthA), int(widthB))

	heightA = np.sqrt( ( (tr[0] - br[0]) ** 2) + ( (tr[1] - br[1]) ** 2) )
	heightB = np.sqrt( ( (tl[0] - bl[0]) ** 2) + ( (tl[1] - bl[1]) ** 2) )

	maxHeight = max(int(heightA), int(heightB))


	# so perspective transform here is taking random four points in that specified order
	# and then map them to (0, 0) and (width - 1, 0) and (width - 1, height - 1), (0, height - 1)
	# order in x-y graph. think this way
	dst = np.array( [ [0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight -1] ], dtype = "float32" )

	# This function gives us the  perspective transformation matrix
	M = cv2.getPerspectiveTransform(rect, dst)
	
	# this function always warps the image and converts the image to the top down approach
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

	return warped

	









