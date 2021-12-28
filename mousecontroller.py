import cv2
import mediapipe as mp
import math
import pyautogui

mp_draw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands = 1)
dia = 30
rad = int(dia/2)
x_screen_max = pyautogui.size()[0]
y_screen_max = pyautogui.size()[1]


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

with mp_hands.Hands(min_detection_confidence = 0.7, min_tracking_confidence = 0.7) as hand:
    while cap.isOpened():
        ret, frame = cap.read()
        #this is an issue with my cam, delete next line of code if webcam feed is inverted
        frame = cv2.flip(frame, 1)

        image = frame
        results = hand.process(image)
        

        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                for id, lm in enumerate(hand_landmark.landmark):
                    h,w,c = image.shape
                    cx,cy = int(lm.x*w), int(lm.y*h)
                    if id==8:       
                        cv2.circle(image,(cx,cy),rad,(255,0,255),cv2.FILLED)
                        f1 = (cx,cy)
                    elif id==4:       
                        cv2.circle(image,(cx,cy),rad,(255,0,255),cv2.FILLED)
                        ft = (cx,cy)
                x_scaled = int((x_screen_max*f1[0])/640) 
                y_scaled = int((y_screen_max*f1[1])/480)
                xm = pyautogui.position()[0]
                ym = pyautogui.position()[1]
                if ([xm,ym] != [x_scaled,y_scaled]):
                    pyautogui.moveTo(x_scaled, y_scaled, duration=0.001)      
                if(math.sqrt(((f1[0]-ft[0])**2)+((f1[1]-ft[1])**2) )<=dia):
                    r = pyautogui.position()
                    xr = r[0]
                    yr = r[1]
                    pyautogui.click(xr, yr)        
                mp_draw.draw_landmarks(image, hand_landmark, mp_hands.HAND_CONNECTIONS) 

        
        cv2.imshow('WebcamFeed', image)

 


        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()    
