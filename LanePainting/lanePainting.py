import cv2
import numpy as np
#Create global for last known left amd right lane
lastLeft=[]
lastRight=[]

#Function for selecting region of knterest
def selectRegion(image,region):
	#Bounds of region defined by x and y
    original=image.copy()
    img=image.copy()
    #Create shape using bounds
    vertices = np.array([[region[0], region[2], region[3], region[1]]], dtype=np.int32)
    #Fill shape with color then mask to return roi
    cv2.fillPoly(img,vertices,255)
    mask=cv2.inRange(img,np.array([254,0,0]),np.array([255,0,0]))
    roi=cv2.bitwise_and(original,original,mask=mask)
    return roi

#Get the raw output of houghLinesP and return image with lines drawn
def rawLines(img,hsv):
	#Create color mask for lane lines
    minYellow = np.array([15,100,100])
    maxYellow = np.array([30,255,255])
    maskYellow =cv2.inRange(hsv,minYellow,maxYellow)
    minWhite = np.array([0,0,240])
    maxWhite = np.array([255,80,255])
    maskWhite=cv2.inRange(hsv,minWhite,maxWhite)
    mask=cv2.bitwise_or(maskYellow,maskWhite)
    #Blur mask then edge detect
    blur=cv2.GaussianBlur(mask,(9,9),0)
    edge=cv2.Canny(blur,100,150)
    #Get hough lines and paint all on the image
    lines=cv2.HoughLinesP(edge, rho=1, theta=np.pi/180, threshold=20, minLineLength=50, maxLineGap=30)
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img,(x1,y1),(x2,y2),(255,0,255),2)
    return img

#Get an average left and right lane line
def getLines(img,hsv):
	#Define global lane lines
    global lastLeft
    global lastRight
    #Mask for yellow and white lane lines
    minYellow = np.array([15,100,100])
    maxYellow = np.array([30,255,255])
    maskYellow =cv2.inRange(hsv,minYellow,maxYellow)
    minWhite = np.array([0,0,230])
    maxWhite = np.array([255,80,255])
    maskWhite=cv2.inRange(hsv,minWhite,maxWhite)
    mask=cv2.bitwise_or(maskYellow,maskWhite)
    #Blur the mask and run edge setection on blur
    blur=cv2.GaussianBlur(mask,(9,9),0)
    edge=cv2.Canny(blur,100,150)
    #Get hough lines
    lines=cv2.HoughLinesP(edge, rho=1, theta=np.pi/180, threshold=20, minLineLength=50, maxLineGap=30)
    #Define variables for averaging lines
    leftLines=[]
    rightLines=[]
    leftWeights=[]
    rightWeights=[]
    try:
        length=len(lines)
    except Exception as e:
        cv2.line(img,(lastRight[0],lastRight[1]),(lastRight[2],lastRight[3]),(255,0,255),3)
        cv2.line(img,(lastLeft[0],lastLeft[1]),(lastLeft[2],lastLeft[3]),(255,0,255),3)
        return img 
    for line in lines:
        for x1,y1,x2,y2 in line:
        	#If the line is straight go to next line
            if x2==x1:
                continue
            slope=float((y2-y1))/float((x2-x1))
            intercept=y1-slope*x1
            #If the line is a left line add to left lines and add length to weight
            #Else do the same for right
            if slope<0:
                leftLines.append((slope,intercept))
                leftWeights.append(((x1-x2)**2+(y1-y2)**2)**.5)
            else:
                rightLines.append((slope,intercept))
                rightWeights.append(((x1-x2)**2+(y1-y2)**2)**.5)
    #Average left and right lanes
    leftLane=np.dot(leftWeights,leftLines)/np.sum(leftWeights)
    rightLane=np.dot(rightWeights,rightLines)/np.sum(rightWeights)
    y1=int(img.shape[0])
    y2=int(y1*.6)
    #If a new left lane has been found paint it
    #Else paint last known left
    if len(leftWeights)>0 and leftLane[0]!=0:
        x1=int((y1-leftLane[1])/leftLane[0])
        x2=int((y2-leftLane[1])/leftLane[0])
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        lastLeft=[x1,y1,x2,y2]
    elif len(lastLeft)!=0:
        cv2.line(img,(lastLeft[0],lastLeft[1]),(lastLeft[2],lastLeft[3]),(255,0,255),3)
    #If a new left lane has been found paint it
    #Else paint last known left
    if len(rightWeights)>0 and rightLane[0]!=0:
        x1=int((y1-rightLane[1])/rightLane[0])
        x2=int((y2-rightLane[1])/rightLane[0])
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        lastRight=[x1,y1,x2,y2]
    elif len(lastRight)!=0:
        cv2.line(img,(lastRight[0],lastRight[1]),(lastRight[2],lastRight[3]),(255,0,255),3)
    return img

def main():
    filePath=raw_input("Input the filePath:")
    if "mp4" not in filePath:
        # Code for running with images
        img = cv2.imread(filePath)
        dimensions=[[120,img.shape[0]],[880,img.shape[0]],[415,340],[550,340]]
        roi=cv2.cvtColor(selectRegion(img,dimensions),cv2.COLOR_BGR2HSV)
        new=getLines(img.copy(),roi)
        cv2.imshow('frame',new)
        cv2.imwrite("output.png",new)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    elif "mp4" in filePath:
        # Code for running with a video
        cap=cv2.VideoCapture(filePath)
        out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (int(cap.get(3)),int(cap.get(4))))
        if "challenge" in filePath:
            while(cap.isOpened()):
                ret,img=cap.read()
                dimensions=[[175,img.shape[0]],[1180,img.shape[0]],[600,429],[745,445]]
                roi=cv2.cvtColor(selectRegion(img,dimensions),cv2.COLOR_BGR2HSV)
                new=getLines(img.copy(),roi)
                cv2.imshow("Frame",new)
                out.write(new)
                if cv2.waitKey(20) & 0xFF == ord('q'):
                    break
        else:
            while(cap.isOpened()):
                ret,img=cap.read()
                dimensions=[[120,img.shape[0]],[880,img.shape[0]],[415,340],[550,340]]
                roi=cv2.cvtColor(selectRegion(img,dimensions),cv2.COLOR_BGR2HSV)
                new=getLines(img.copy(),roi)
                cv2.imshow("Frame",new)
                out.write(new)
                if cv2.waitKey(20) & 0xFF == ord('q'):
                    break
        out.release()
        cap.release()


main()
