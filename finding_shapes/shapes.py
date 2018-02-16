import numpy as np
import cv2
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image in which we want to find shapes")
args = vars(ap.parse_args())


image = cv2.imread(args["image"])
original = image.copy()

lower = np.array([0, 0, 0])
upper = np.array([15, 15, 15])

# here [0, 0, 0] means we are sepcifying black color
# and [15, 15, 15] means somewhere in a dark grey color 
# The cv2.inRange fn takes the image, the lower and the upper bounds and find all the pixels in that range
shapeMask = cv2.inRange(image, lower, upper)

(_, cnts, _) = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

print("I found %d black shapes" %(len(cnts)))
cv2.imshow("Mask", shapeMask)

for c in cnts:
	cv2.drawContours(image, [c], -1, (0, 255, 0), 2)

cv2.imshow("Image", image)
cv2.waitKey(0)