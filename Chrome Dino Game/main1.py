import cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector
import time
from directkeys import PressKey, ReleaseKey, space_pressed

detector=HandDetector(detectionCon=0.8, maxHands=1)
time.sleep(2)
current_key_pressed=set()
space_key_pressed=space_pressed
video=cv2.VideoCapture(0)
while True:
    ret,frame=video.read()
    keyPressed=False
    spacePressed=False
    key_count=0
    key_pressed=0
    hand,image=detector.findHands(frame)
    if hand:
        lmList=hand[0]
        fingerUp=detector.fingersUp(lmList)
        if fingerUp==[0,0,0,0,0]:
            cv2.putText(frame, "Jump", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 4)
            PressKey(space_key_pressed)
            spacePressed=True
            current_key_pressed.add(space_key_pressed)
            key_pressed=space_key_pressed
            keyPressed=True
            key_count+=1
        elif fingerUp==[0,1,0,0,0]:
            cv2.putText(frame, "Not jumping", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 4)
        elif fingerUp==[0,1,1,0,0]:
            cv2.putText(frame, "Not jumping", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 4)
        elif fingerUp==[0,1,1,1,0]:
            cv2.putText(frame, "Not jumping", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 4)
        elif fingerUp==[0,1,1,1,1]:
            cv2.putText(frame, "Not jumping", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 4)
        elif fingerUp==[1,1,1,1,1]:
            cv2.putText(frame, "Not jumping", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 4)
        if not keyPressed and len(current_key_pressed) != 0:
            for key in current_key_pressed:
                ReleaseKey(key)
            current_key_pressed = set()
        elif key_count==1 and len(current_key_pressed)==2:    
            for key in current_key_pressed:             
                if key_pressed!=key:
                    ReleaseKey(key)
            current_key_pressed = set()
            for key in current_key_pressed:
                ReleaseKey(key)
            current_key_pressed = set()
    cv2.imshow("Video", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video.release()
cv2.destroyAllWindows()