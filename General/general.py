#Caleb Riggs
import cv2
import numpy as np
#Load the image and resize so it is easier to view
fileName=raw_input("Enter the file name:")
raw_input("Use the left and right arrows to scroll through images.\nPress any key to exit.\nHit enter to continue.")
img = cv2.imread(fileName)
img=cv2.resize(img,(0,0),fx=.25,fy=.25)

#Create HSV image to use color filtering
hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
#Create High red mask
minHighRed = np.array([170,50,50])
maxHighRed = np.array([180,255,255])
maskHighRed=cv2.inRange(hsv,minHighRed,maxHighRed)
#Create Low red mask
minLowRed = np.array([0,50,50])
maxLowRed = np.array([10,255,255])
maskLowRed=cv2.inRange(hsv,minLowRed,maxLowRed)
#Or the high and low mask together to create one red mask
cv2.bitwise_or(maskLowRed,maskHighRed,maskLowRed)
red=cv2.bitwise_and(img,img,mask=maskLowRed)
#Create green mask
minGreen = np.array([50,50,50])
maxGreen = np.array([70,255,255])
maskGreen=cv2.inRange(hsv,minGreen,maxGreen)
green=cv2.bitwise_and(img,img,mask=maskGreen)
#Create blue mask
minBlue = np.array([110,50,50])
maxBlue = np.array([130,255,255])
maskBlue=cv2.inRange(hsv,minBlue,maxBlue)
blue=cv2.bitwise_and(img,img,mask=maskBlue)
'''
#This section will do color filtering as oppesed to masking above
red=img.copy()
red[:,:,0]=0
red[:,:,1]=0
green=img.copy()
green[:,:,0]=0
green[:,:,2]=0
blue=img.copy()
blue[:,:,1]=0
blue[:,:,2]=0
'''
#Blur the image and grayscale the blurred image
blur = cv2.GaussianBlur(img,(5,5),0)
grayImg = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
#Run canny edge detecion on blurred grayscale image
edges = cv2.Canny(grayImg,100,150)
#Create array of all images then initialize loop for scrolling
temp=[img,red,green,blue,blur,grayImg,edges]
keep=1
pos=0
while(keep):
    cv2.imshow("Images",temp[pos])
    key=cv2.waitKey(0)
    cv2.destroyAllWindows()
    #If right arrow pressed go to next image
    if key== 83 and pos!=(len(temp)-1):
        pos+=1
    #If left arrow pressed go to previous image
    elif key==81 and pos!=0:
        pos-=1
    else:
        keep=0
