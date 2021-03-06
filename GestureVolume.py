import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
import pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

###################################
wCam, hCam = 640, 480
###################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
cTime = 0

dectector = htm.handDetector(detectionCon=0.75) 

####
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
 IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange =volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0 
volBar = 400
volPer = 0
####

while True:
        success,img = cap.read()

        #Find hand

        img = dectector.findHands(img)
        lmlist = dectector.findPosition(img, draw = False)
        if len(lmlist) !=0:

            #Filter based on size

            #find distancen btw index(8)-thumb(4) 

            #convert length

            #reduce res to smooth
            #check fingers up 
            #if pinky is dwn set vol
            #Drawing
            #Frame rate



            
         #print (lmlist[4], lmlist[8])

         x1, y1 = lmlist[4][1], lmlist[4][2]
         x2, y2 = lmlist[8][1], lmlist[8][2]
         cx, cy = (x1+x2)//2, (y1+y2)//2

         cv2.circle(img,(x1,y1),10,(255,69,0),cv2.FILLED)#index4
         cv2.circle(img,(x2,y2),10,(255,69,0),cv2.FILLED)#index8
         cv2.circle(img,(cx,cy),10,(255,69,0),cv2.FILLED)#midpt

         cv2.line(img, (x1,y1),(x2,y2),(255,0,255),3 )#i4-i8 line 

         length = math.hypot(x2-x1,y2-y1)
         #print(length)
        
         #handrange 50to300
         #vol Range -65to0 

         vol=np.interp(length,[50,300],[minVol, maxVol])
         volBar=np.interp(length,[50,300],[400, 150])
         volPer=np.interp(length,[50,300],[0, 100])
         print(int(length),vol)
         volume.SetMasterVolumeLevel(vol, None)

         if length<50 :
             cv2.circle(img,(cx,cy),10,(69,69,69), cv2.FILLED)
 
        cv2.rectangle (img, (50,150), (85, 400), (0,0,255), 3)
        cv2.rectangle (img, (50,int(volBar)), (85, 400), (0,255,0), cv2.FILLED)
        cv2.putText(img, f'{int(volPer)}  %',(40,450), cv2.FONT_HERSHEY_DUPLEX,0.65,(255,0,0), 3)
        
        
        cTime= time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, f'FPS: {int(fps)}',(3,20), cv2.FONT_HERSHEY_DUPLEX,0.65,(255,69,0), 2)

        cv2.imshow("Img", img)
        cv2.waitKey(1)