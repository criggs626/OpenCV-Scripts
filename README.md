# OpenCV-Scripts
This is a git repo with a few OpenCV scripts written in Python 2.7 to demonstrate
the code. The current existing scripts are as follows.
- General Functions
- Lane Painting

## General Functions
These are simply general functions in OpenCV, it will take an image as an input file.
Once a file has been input it will apply a red mask, blue mask, and green mask.
After this the original image will be grayscaled then a gaussian blur is applied.
The blurred gray image is then used for canny edge detection.
These images can all be displayed and scrolled through.

## Lane Painting
This script is built to paint yellow and white lane lines on a road.
A region of interest is created first to allow broader color masking.
The mask is then blurred and run through canny edge detection. Once this step
is complete the Probabilistic Hough lines function is used. The results of this
are separated into two groups left lanes and right lanes. These two groups are then
averaged and painted onto the original image.
