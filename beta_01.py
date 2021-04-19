####################################
#
# DENNA VERSION FUNGERAR BRA!!! bara mail delen kvar
####################################

import numpy as np
import cv2
import datetime
import time
import os
import subprocess

import threading 

move = 0
cap = cv2.VideoCapture(0)
#fourcc = cv2.VideoWriter_fourcc(*'XVID') 
codec = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('/home/pi/motion_detection/videos/output2.avi', codec, 20.0, (640, 480)) 
t0 = time.time()
static_back = None

while True: ###YES FUNKAR ATT SPELA IN VIDEO NU, DOCK SPELAR DEN HELA TIDEN

    check, frame = cap.read()
    frame2 = cv2.flip(frame, -1)

    scene = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    scene = cv2.GaussianBlur(scene, (21, 21), 0)
    #gray = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

    
  #  cv2.putText(frame2,"Hello!!!", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,0),2,cv2.LINE_4)

    if static_back is None:
        static_back = scene
        continue

    diff_frame = cv2.absdiff(static_back, scene)
    thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1] 
    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2) 

    cnts,_ = cv2.findContours(thresh_frame.copy(),  
                       cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
  
    for contour in cnts: 
        if cv2.contourArea(contour) < 1000: 
            continue

        (x, y, w, h) = cv2.boundingRect(contour) 
        
        # making green rectangle arround the moving object 
        cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.putText(frame2,"Intruder!!!", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255),2,cv2.LINE_4)
        roi = frame2[y:y+h, x:x+w]
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y_%H-%M-%S')
        # if the detection is on sized then save the image 
        if (w > h ) and (y + h) > 50 and (y + h) < 550:
            cv2.imwrite(st+".jpg", frame2)
            
            t1 = time.time() # current time
            num_seconds = t1 - t0
            out.write(frame2) # diff
            if num_seconds > 30:  # e.g. break after 30 seconds
                break
                
                
  
            
            move = 2

        
            #Använd samma vilkor fast tvärtom
            
         

    cv2.imshow("LIVE FEED", frame2) 
    #cv2.imshow('frame', frame2)
  
    key = cv2.waitKey(1) 
    # if q entered whole process will stop 
    if key == ord('q'): 
        if move == 2:

            os.system('/home/pi/motion_detection/mail_send.py')

        #Skicka video
        # if something is movingthen it append the end time of movement 
        print("closing it")
        break
cap.release()
out.release()
cv2.destroyAllWindows()
