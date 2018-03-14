Code to detect the barcode in an image.

We calculate the x- and the y-gradients and subtract them to obtain the region with a high horizontal gradient and a low vertical gradient which is our barcoded region. From there we perform a couple of dilations to remove the unneccessary blobs and make a complete picture, binary invert the image and then draw contours around the barcoded region.

Usage:

From the terminal, type:

```python _filename_ -i _path to image_ ```

example: ```python detect_barcode.py -i images/retina.png```
