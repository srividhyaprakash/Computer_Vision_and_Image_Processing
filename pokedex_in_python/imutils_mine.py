# basic image processing techniques
import cv2
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("-q", "--query", required = True, help = "the image to be parsed")
args = vars(ap.parse_args())


image = cv2.imread(args["query"])
cv2.imshow("original", image)
cv2.waitKey(0)

# prints out the width, height in that order
print(image.shape)

# to preserve the aspect ratio - propotional relationship of the width and the height of the image
# we calculate the aspect ratio
r = 100 / image.shape[1]

# we resize the image to 100pixels width and then old image height * aspect ratio = new height
dim = (100, int(image.shape[0] * r))

# 3rd parameter is the algorithm to use when resizing 
resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
cv2.imshow("resized", resized)
cv2.waitKey(0)

(h,w) = image.shape[:2]
center = (w/2, h/2)

# rotate the image by 180 degrees
M = cv2.getRotationMatrix2D(center, 90, 1.0)
rotated = cv2.warpAffine(image, M, (w, h))
cv2.imshow("rotated", rotated)
cv2.waitKey(0)


# to crop, specify the startY:endY folllowed by startX:endX coordinates. 
# that is all there is to cropping 
# eg: cropped = image[70:170, 440:540]
cropped = rotated[781:1094, 1859:2176]
cv2.imshow("cropped pokemon image", cropped)
cv2.waitKey(0)
# to write a file to disk, openCV writes it as whatever extension we give in the first argument
# eg: cv2.imwrite("thumbnail.png", cropped) 






