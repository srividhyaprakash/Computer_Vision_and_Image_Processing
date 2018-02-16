from searcher import Searcher
from zernike_moments import ZernikeMoments
import imutils
import cv2
import argparse
import _pickle as cPickle
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--index", required = True, help = "Path to where the index file is stored")
ap.add_argument("-q", "--query", required = True, help = "Path to the query image")
args = vars(ap.parse_args())


index = open(args["index"], 'rb').read()
index = cPickle.loads(index)

image = cv2.imread(args["query"])
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image = imutils.resize(image, width = 64)

# we need to prepare our query image by thresholding the image and finding contours.
# threshold the image
thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 7)
# thresh_mean = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 7)

cv2.imshow("thresholded guassian image", thresh)
cv2.waitKey(0)
# cv2.imshow("thresholded mean image", thresh_mean)
# cv2.waitKey(0)

outline = np.zeros(image.shape, dtype = "uint8")
(_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[0]


cv2.drawContours(outline, [cnts], -1, 255, -1)

cv2.imshow("outermost countour", outline)
cv2.waitKey(0)

desc = ZernikeMoments(21)

queryFeatures = desc.describe(outline)

searcher = Searcher(index)

results = searcher.search(queryFeatures)

print("That pokemon is %s" %(results[0][1].upper()))

cv2.imshow("image", image)
cv2.waitKey(0)