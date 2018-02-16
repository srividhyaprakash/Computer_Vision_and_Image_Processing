from zernike_moments import ZernikeMoments
import glob
import _pickle as cPickle
import numpy as np
import cv2
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("-s","--sprites", required = True, help = "path to where the sprites are stored")
ap.add_argument("-i", "--index", required = True, help = "path to where the index file will be stored")
args = vars(ap.parse_args())

# initialize our zernike moments image descriptor.
# Image moments are used to describe objects in a image
# Using Image moments, we can calculate the area of the image, the centroid(center in terms of x,y coordinates)
# cv2 provides Hu moments but zernike moments although affected by scale variance are not affected by the 
# rotation of the object.
# we can perform segmentation to overcome the scale variance problem and feed the segmented image to the zernike_momnets function
# Segmentation - we segment the foreground (the object we are interested in) from the background (the noise) and single it out.
desc = ZernikeMoments(21)
index = {}

# loop over sprite images
for spritePath in glob.glob(args['sprites'] + "/*.png"):
	# parse the pokemon name
	pokemon = spritePath[spritePath.rfind("/") + 1:].replace(".png", "")
	image = cv2.imread(spritePath)
	# read the image and convert it to grayscale
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# pad the image on all four sides with white pixels
	# 15 is padding on each side, to be padded with is value : white pixels
	image = cv2.copyMakeBorder(image, 15, 15, 15, 15, cv2.BORDER_CONSTANT, value = 255)


	# invert the image
	thresh = cv2.bitwise_not(image)

	# the images are white background and pokemon is black. 
	# we convert the white pixels to black and black pixels to white
	# so now previously white pixels (background) are black
	# black pixels (the pokemon, foreground), now white, will have a value > 0, we convert them to white.
	thresh[thresh > 0] = 255

	# now we need the outermost contour - the outline of the pokemon

	outline = np.zeros(image.shape, dtype = "uint8")

	# first argument is the threshold image
	# cv2.RETR_EXTERNAL = return the most external contour
	# cv2.CHAIN_APPROX_SIMPLE = compress and approximate the contour to save memory
	(image, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	# we are sorting and then taking only the outermost largest contour because we only want the outermost contour - outline of the pokemon
	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[0]

	# we draw the outermost contour on our outline image
	cv2.drawContours(outline, [cnts], -1 , 255, -1)

	# calculate the moments using the mahotas library - Zernike moments , wrapper function
	moments = desc.describe(outline)
	index[pokemon] = moments

f = open(args["index"], "wb")
f.write(cPickle.dumps(index))
f.close()















