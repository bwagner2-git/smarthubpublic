import handTrack
import time
import numpy as np
import cv2
from pynput.mouse import Button, Controller
import os
import math

os.system("xrandr | grep \* | cut -d' ' -f4 > resolution.txt") ##get screen size
###do not know what the gamma is for the output default if things go wrong check the text file to see if something is going wrong
f=open('resolution.txt','r')
screenSize=f.readlines()[0].replace('\n','').split('x')
screenSize[0]=int(screenSize[0])
screenSize[1]=int(screenSize[1])

########
camWidth, camHeight = 640,480
frameReduc=100
########

a=handTrack.featureDetector()
cap=cv2.VideoCapture(0)
cap.set(3,camWidth)
cap.set(4,camHeight)
mouse=Controller()

###mouse smoothening###
currentLocationx, currentLocationy = 0, 0
previousLocationx, previousLocationy = 0, 0
smoothening=2
#######################

percentChange=None
while True:
    success, frame=cap.read()
    features=a.getFeature(frame)
    cv2.rectangle(frame, (100,frameReduc),(camWidth-100,camHeight-100),(255,0,255),2)
    if features:
        indexFingerx=features[12][0]
        indexFingery=features[12][1]
        wristx=features[0][0]
        wristy=features[0][1]
        currentDistance=math.sqrt((indexFingerx-wristx)**2+(indexFingery-wristy)**2)
        try:
            percentChange=abs((currentDistance-previousDistance)/previousDistance)
            # if percentChange>=.6:
            #     print("updated to: " + str(percentChange))
            previousDistance=currentDistance
        except:
            previousDistance=currentDistance
        xCon=np.interp(wristx,(100,camWidth-100),(0,screenSize[0]))
        yCon=np.interp(wristy,(frameReduc,camHeight-100),(0,screenSize[1]))

        currentLocationx=previousLocationx+(xCon-previousLocationx)/smoothening
        currentLocationy=previousLocationy+(yCon-previousLocationy)/smoothening
        mouse.position=(screenSize[0]-currentLocationx,currentLocationy)
        previousLocationx, previousLocationy=currentLocationx, currentLocationy
        if percentChange:
            if percentChange>=.6:
                mouse.click(Button.left,1)

    cv2.imshow("track", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        cv2.destroyAllWindows()
        break

cap.release()

#from video
#showed how to do smoothening
#showed how to invert 
#showed how to do rectange on screen





