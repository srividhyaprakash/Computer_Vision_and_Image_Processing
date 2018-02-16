from transform import four_point_transform
import argparse
import cv2
import numpy as np


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Image to warp")
ap.add_argument("-c", "--coords", help = "comma separated list of source points")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])


pts = np.array(eval(args["coords"]), dtype = "float32")

warped = four_point_transform(image, pts)

cv2.imshow("Image", image)
cv2.imshow("Warped Image", warped)

cv2.waitKey(0)