import mediapipe as mp
import cv2
import numpy as np
import uuid
import os
import time

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
# help(mp_hands.Hands)
cap = cv2.VideoCapture("test.mp4")
#cap = cv2.VideoCapture(0)
#cap.set(3,640)
#cap.set(4,480)
cap.set(3,40)
cap.set(4,30)
with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands: 
    while cap.isOpened():
       
        ret, frame = cap.read()
         # Resize the image to 640x480
        resized_image = cv2.resize(frame, (640, 480))
        # BGR 2 RGB
        image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        
        # # Flip on horizontal
        # image = cv2.flip(image, 1)
        
        # Set flag
        image.flags.writeable = False
        
        # Detections
        results = hands.process(image)
        
        # Set flag to true
        image.flags.writeable = True
        
        # RGB 2 BGR
        resized_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Detections
        # print(results)
        
        # Rendering results
        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS, 
                                        mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                        mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                                         )
                
        # print(results.multi_hand_landmarks)
        print(results.multi_hand_world_landmarks)
        # print(type(results.multi_hand_world_landmarks))
        print(results.multi_handedness)
        
        
        # time.sleep(1)
        cv2.imshow('Hand Tracking', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

