Code to warp the given image to obtain a top-down view

Prior Steps:

First, open a new file using OpenCV. If we scroll through the image, we get the coordinates of the cursor in the bottom-left part of the image.

Note down the coordinates for the top-left, top-right, bottom-right and bottom-left corners in that order. 

Usage: 

Open up the terminal, navigate to these file locations and type in the terminal:

`python transform_example.py -i _pathToImage_ -c _coordinatesAsAList_`


example : `python transform_example.py -i images/example_01.png -c "[(73, 239), (356, 117), (475, 265), (187, 443)]"`
