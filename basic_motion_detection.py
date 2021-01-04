import numpy as np
import cv2
import datetime

cap = cv2.VideoCapture(0)

static_back = None

while True:

    check, frame = cap.read()
    frame2 = cv2.flip(frame, -1)

    scene = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    scene = cv2.GaussianBlur(scene, (21, 21), 0)
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
        cv2.putText(frame2,"Intruder!!!", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,255),2,cv2.LINE_4)
        roi = frame2[y:y+h, x:x+w]
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y_%H-%M-%S')
        # if the detection is on sized then save the image 
        if (w > h ) and (y + h) > 50 and (y + h) < 550:
            cv2.imwrite(st+"opencv.jpg", roi)

    cv2.imshow("LIVE FEED", frame2) 
  
    key = cv2.waitKey(1) 
    # if q entered whole process will stop 
    if key == ord('q'): 
        # if something is movingthen it append the end time of movement 
        print("closing it")
        break


cv2.destroyAllWindows()
