1. Image from the command line is taken as input.
2. Image converted to grayscale.
3. Introduced noise (GaussianBlur) so as to make the edge detection more robust. Note: A bilateral filter could have been used and it preserves edges much better but in this application, our document is the only object in the image and hence both achieve comparable results.
4. Find the contours of the image and take the outermost (largest) contour.
5. Order the (x, y) coordinates of the outermost contour in the following format (top-right, top-left, bottom-left, bottom-right)
6. Apply a perspective transform and warp the image while maintaining scale invariance to obtain a top-down "birds-eye" view of the document.
7. Apply "threshold_local" function to give it a "scanned" feel


Usage:

From the command line, type : `python scanner.py -i "path to the image"`
