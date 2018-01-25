# Lane Painting
lanePainting.py is program written in pythonb 2.7 that uses OpenCV to paint the lanes on a road.
The process goes as listed below.
## Steps Taken
### 1) Load image
The image is loaded on line 86 of the program
``` python
img = cv2.imread("src/solidWhiteCurve.png")
```
### 2) Select Region of interest
The selectRegion function is used to get the region of interest. This function takes
the original image twice as the input (Why it doesn't copy the image within don't ask).
The region is defined in the selectRegion function on lines 7-10.
``` python
bottomLeft=[120,img.shape[0]]
bottomRight=[880,img.shape[0]]
topLeft=[415,340]
topRight=[550,340]
```
The selectRegion function returns the region and is immediately turned to HSV for the next part.
### 3) Get Lines
This step is broken down into multiple parts but is one function call.
##### A) Color Mask for lanes
We color mask yellow and white that way we can view the lane lines.
##### B) Blur on Color Mask
Take the color mask and blur it to make the lane lines smoother.
##### C) Canny Edge on Blurred image
Run canny edge detection on the blurred mask to make the lanes easier to be detected hough lines.
##### D) Probabilistic Hough Lines on Edge image
Run probabilistic hough lines on the edge image.
##### E) Average Probabilistic Hough Lines
Group lines by left and right then average the lines
##### F) Paint Average
Finally paint the averaged lines onto the original image.

## Output
#### Original
![Original Solid White IMG](https://raw.github.com/criggs626/OpenCV-Scripts/master/LanePainting/src/solidWhiteCurve.png)
![Original Solid Yellow IMG](https://raw.github.com/criggs626/OpenCV-Scripts/master/LanePainting/src/solidYellowLeft.png)
#### Painted
![Original Solid White IMG](https://raw.github.com/criggs626/OpenCV-Scripts/master/LanePainting/output/solidWhiteCurve.png)
![Original Solid Yellow IMG](https://raw.github.com/criggs626/OpenCV-Scripts/master/LanePainting/output/solidYellowLeft.png)
