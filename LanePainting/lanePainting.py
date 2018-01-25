import cv2
import numpy as np
lastLeft=[]
lastRight=[]

def selectRegion(original,img):
    bottomLeft=[120,img.shape[0]]
    bottomRight=[880,img.shape[0]]
    topLeft=[415,340]
    topRight=[550,340]
    vertices = np.array([[bottomLeft, topLeft, topRight, bottomRight]], dtype=np.int32)
    cv2.fillPoly(img,vertices,255)
    mask=cv2.inRange(img,np.array([254,0,0]),np.array([255,0,0]))
    roi=cv2.bitwise_and(original,original,mask=mask)
    return roi

def rawLines(img,hsv):
    minYellow = np.array([15,100,100])
    maxYellow = np.array([30,255,255])
    maskYellow =cv2.inRange(hsv,minYellow,maxYellow)
    minWhite = np.array([0,0,240])
    maxWhite = np.array([255,80,255])
    maskWhite=cv2.inRange(hsv,minWhite,maxWhite)
    mask=cv2.bitwise_or(maskYellow,maskWhite)
    blur=cv2.GaussianBlur(mask,(9,9),0)
    edge=cv2.Canny(blur,100,150)
    lines=cv2.HoughLinesP(edge, rho=1, theta=np.pi/180, threshold=20, minLineLength=50, maxLineGap=30)
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img,(x1,y1),(x2,y2),(255,0,255),2)
    return img

def getLines(img,hsv):
    global lastLeft
    global lastRight
    minYellow = np.array([15,100,100])
    maxYellow = np.array([30,255,255])
    maskYellow =cv2.inRange(hsv,minYellow,maxYellow)
    minWhite = np.array([0,0,230])
    maxWhite = np.array([255,80,255])
    maskWhite=cv2.inRange(hsv,minWhite,maxWhite)
    mask=cv2.bitwise_or(maskYellow,maskWhite)
    blur=cv2.GaussianBlur(mask,(9,9),0)
    edge=cv2.Canny(blur,100,150)
    lines=cv2.HoughLinesP(edge, rho=1, theta=np.pi/180, threshold=20, minLineLength=50, maxLineGap=30)
    leftLines=[]
    rightLines=[]
    leftWeights=[]
    rightWeights=[]
    for line in lines:
        for x1,y1,x2,y2 in line:
            if x2==x1:
                continue
            slope=float((y2-y1))/float((x2-x1))
            intercept=y1-slope*x1

            if slope<0:
                leftLines.append((slope,intercept))
                leftWeights.append(((x1-x2)**2+(y1-y2)**2)**.5)
            else:
                rightLines.append((slope,intercept))
                rightWeights.append(((x1-x2)**2+(y1-y2)**2)**.5)

    leftLane=np.dot(leftWeights,leftLines)/np.sum(leftWeights)
    rightLane=np.dot(rightWeights,rightLines)/np.sum(rightWeights)
    y1=int(img.shape[0])
    y2=int(y1*.6)
    if len(leftWeights)>0 and leftLane[0]!=0:
        x1=int((y1-leftLane[1])/leftLane[0])
        x2=int((y2-leftLane[1])/leftLane[0])
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        lastLeft=[x1,y1,x2,y2]
    elif len(lastLeft)!=0:
        cv2.line(img,(lastLeft[0],lastLeft[1]),(lastLeft[2],lastLeft[3]),(255,0,255),3)
    if len(rightWeights)>0 and rightLane[0]!=0:
        x1=int((y1-rightLane[1])/rightLane[0])
        x2=int((y2-rightLane[1])/rightLane[0])
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        lastRight=[x1,y1,x2,y2]
    elif len(lastRight)!=0:
        cv2.line(img,(lastRight[0],lastRight[1]),(lastRight[2],lastRight[3]),(255,0,255),3)
    return img

# Code for running with images
img = cv2.imread("src/solidWhiteCurve.png")
roi=cv2.cvtColor(selectRegion(img.copy(),img.copy()),cv2.COLOR_BGR2HSV)
new=getLines(img.copy(),roi)
cv2.imshow('frame',new)
cv2.waitKey(0)
cv2.destroyAllWindows()
#ROI for images
#bottomLeft=[120,img.shape[0]]
#bottomRight=[880,img.shape[0]]
#topLeft=[415,340]
#topRight=[550,340]
'''
# Code for running with a video
#img = cv2.imread("images/solidYellowLeft.jpg")
cap=cv2.VideoCapture("images/challenge.mp4")
while(cap.isOpened()):
    ret,img=cap.read()
    roi=cv2.cvtColor(selectRegion(img.copy(),img.copy()),cv2.COLOR_BGR2HSV)
    new=getLines(img.copy(),roi)
    cv2.imshow("Frame",new)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
#ROI for challenge.mp4
#bottomLeft=[175,img.shape[0]]
#bottomRight=[1180,img.shape[0]]
#topLeft=[600,429]
#topRight=[745,445]
'''
