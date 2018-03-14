Code to detect the barcode in a video.

We calculate the x- and the y-gradients and subtract them to obtain the region with a high horizontal gradient and a low vertical gradient which is our barcoded region. From there we perform a couple of dilations to remove the unnecessary blobs and make a complete picture, binary invert the image and then draw contours around the barcoded region.

The same procedure is done on a per frame basis and the algorithm is robust to detect barcodes even with the object in the video skewed up to an angle of 30 degrees.

Usage:

From the terminal, type:

python _filename_ -v _path to video_ (optional)

example: python real_time_detect.py 
