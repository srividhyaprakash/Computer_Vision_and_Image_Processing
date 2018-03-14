Code to find the brightest spot in an image.

We introduce noise to the image so that our code is more robust in finding the brightest spot rather than the brightest pixel. Radius is the radius over which we want to average our brightest spot Usage:

From the terminal, type:

```python _filename_ -i _path to image_ -r _number_```

example: ```python bright.py -i images/retina.png -r 21```
