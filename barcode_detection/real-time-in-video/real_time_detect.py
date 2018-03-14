import numpy as np
import cv2
import argparse
import simple_barcode_detect

ap = argparse.ArgumentParser()
ap.add_argument("-v","--video", help = "path to the optional video")
args = vars(ap.parse_args())


if not args.get("video", False):
	camera = cv2.VideoCapture(0)

else:
	camera = cv2.VideoCapture(args["video"])


while True:

	# (boolean, frame in the video)
	(grabbed, frame) = camera.read()

	if not grabbed:
		break

	box = simple_barcode_detect.detect(frame)
	
	if box is not None:
		cv2.drawContours(frame, [box], -1, (0, 255, 0), 2)

	cv2.imshow("frame", frame)

	key = cv2.waitKey(1) & 0xFF
	if  key == ord("q"):
		break

camera.release()
cv2.destroyAllWindows()

