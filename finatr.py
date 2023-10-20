import mediapipe as mp
import cv2
import numpy as np
import pyautogui
import uuid
import os

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

screenwidth, screenheight = pyautogui.size()



cap = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands: 
    while cap.isOpened():
        ret, frame = cap.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        
        frame_height, frame_width, _ = frame.shape
        
        xconst = screenwidth / frame_width
        yconst = screenheight / frame_height

        image.flags.writeable = False
        results = hands.process(image)

        image.flags.writeable = True

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        print(results)

        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS, 
                                        mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                        mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                                         )

                index_finger_landmark = results.multi_hand_landmarks[0].landmark[8]
                Thumb_landmark = results.multi_hand_landmarks[0].landmark[4]
                MF_landmark = results.multi_hand_landmarks[0].landmark[12]
                ringfinger_landmark = results.multi_hand_landmarks[0].landmark[16]
                
                
                # Get the coordinates of the index finger landmark point ke liye.
                index_finger_x = int((index_finger_landmark.x * frame.shape[1])*xconst)
                index_finger_y = int((index_finger_landmark.y * frame.shape[0])*yconst)
                
                #reference ke liye
                thumb_x = int(Thumb_landmark.x*frame.shape[1])
                thumb_y = int(Thumb_landmark.y * frame.shape[0])
                
                #left click
                mf_x = int(MF_landmark.x * frame.shape[1])
                mf_y = int(MF_landmark.y * frame.shape[0])
                
                #right click
                rf_x = int(ringfinger_landmark.x * frame.shape[1])
                rf_y = int(ringfinger_landmark.y * frame.shape[0])
                
                '''
                print('Index finger coordinates:', index_finger_x, index_finger_y)
                print('Thumb finger coordinates:', thumb_x, thumb_y)
                print('Middle finger coordinates:', mf_x, mf_y)
                print('Ring finger coordinates:', rf_x, rf_y)
                '''
                
                '''
                cv2.circle(img=frame, center=(index_finger_x,index_finger_y), radius=50, color=(0, 0, 255))
                cv2.circle(img=frame, center=(mf_x,mf_y), radius=50, color=(0, 0, 255))
                cv2.circle(img=frame, center=(rf_x,rf_y), radius=50, color=(0, 0, 255))
                cv2.circle(img=frame, center=(thumb_x,thumb_y), radius=50, color=(0, 0, 255))            
                '''
                pyautogui.moveTo(index_finger_x ,index_finger_y)
                if abs(thumb_y - mf_y ) < 20: 
                            print("click")
                            pyautogui.click(index_finger_x, index_finger_y)
                            pyautogui.sleep(1)
                if abs(thumb_y - rf_y ) < 20:
                            print("Right click")
                            pyautogui.click(button="right", x = index_finger_x, y = index_finger_y)
                            pyautogui.sleep(1)
                
                
        cv2.imshow('Hand Tracking', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()