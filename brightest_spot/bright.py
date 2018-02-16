import numpy as np
import cv2
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to image in which we want to find the brightest spot")
ap.add_argument("-r", "--radius",type = int, required = True, help = "radius of the gaussian blur; must be odd")
args = vars(ap.parse_args())


image = cv2.imread(args["image"])
orig = image.copy()

gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)


# The naive way without any pre-processing feeding the image to minMaxLoc
# minMaxLoc() is the function that locates the pixel with the lowest intensity and the highest intensity
# it returns the values of min and max intensity and also the (x,y) coordinates

(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)

cv2.circle(image, maxLoc, args["radius"], (255, 0 , 0), 2)

cv2.imshow("Naive", image)

# The more robust method is to apply a gaussian blur as a pre-prcoessing step
# playing around with the radius is key for the gaussian blur to work and is heavily dependent on the dataset
# gaussianBlur if applied, then the image is less susceptible to noise and hence we are able to better predict the brightest spot
# gaussianBlur effectively averages regions within the specified radius instead of considering a single pixel value. 
# That is why we specify the radius

gray = cv2.GaussianBlur(gray, (args["radius"], args["radius"]), 0)
(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
image = orig.copy()
cv2.circle(image, maxLoc, args["radius"], (255, 0, 0), 2)

cv2.imshow("Robust", image)
cv2.waitKey(0)