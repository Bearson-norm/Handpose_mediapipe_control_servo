import cv2 # type: ignore
import mediapipe as mp # type: ignore
import math
import numpy as np # type: ignore
import time

#--------------
  
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# Webcam Setup
wCam, hCam = 640, 480
#cam = cv2.VideoCapture("test.mp4")
cam = cv2.VideoCapture(0)
cam.set(3,wCam)
cam.set(4,hCam)

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

  while cam.isOpened():
    success, image = cam.read()
    image = cv2.resize(image, (640, 480))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style()
            )

    # multi_hand_landmarks method for Finding postion of Hand landmarks      
    lmList = []
    if results.multi_hand_landmarks:
      myHand = results.multi_hand_landmarks[0]
      #print(myHand)
      for id, lm in enumerate(myHand.landmark):
        h, w, c = image.shape
        cx, cy = int(lm.x * w), int(lm.y * h)
        lmList.append([id, cx, cy])          
    
    # print(lmList)
    # Menentukan jari2 dengan pangkal tangkan
    if len(lmList) != 0:
      x1, y1 = lmList[4][1], lmList[4][2] # ibu jari
      x2, y2 = lmList[0][1], lmList[0][2] # pangkal tangan
      x3, y3 = lmList[8][1], lmList[8][2] # telunjuk
      x4, y4 = lmList[12][1], lmList[12][2] # jari tengah
      x5, y5 = lmList[16][1], lmList[16][2] # jari manis
      x6, y6 = lmList[20][1], lmList[20][2] # jari kelingking

      # Marking Thumb and Index finger
      cv2.circle(image, (x1,y1),15,(255,255,255))  
      cv2.circle(image, (x2,y2),15,(255,255,255))  
      cv2.circle(image, (x3,y3),15,(255,255,255))  
      cv2.circle(image, (x4,y4),15,(255,255,255))  
      cv2.circle(image, (x5,y5),15,(255,255,255))  
      cv2.circle(image, (x6,y6),15,(255,255,255))

      cv2.line(image,(x1,y1),(x2,y2),(255,0,0),3)
      cv2.line(image,(x3,y3),(x2,y2),(255,0,0),3)
      cv2.line(image,(x4,y4),(x2,y2),(255,0,0),3)
      cv2.line(image,(x5,y5),(x2,y2),(255,0,0),3)
      cv2.line(image,(x6,y6),(x2,y2),(255,0,0),3)
      
      # ibu jari
      length = math.hypot(x2-x1,y2-y1)
      if length < 50:
        cv2.line(image,(x1,y1),(x2,y2),(0,0,0),3)
      # telunjuk
      length1 = math.hypot(x2-x3,y2-y3)
      if length1 < 50:
        cv2.line(image,(x3,y3),(x2,y2),(0,0,0),3)
      # jari tengah
      length2 = math.hypot(x2-x4,y2-y4)
      if length2 < 50:
        cv2.line(image,(x4,y4),(x2,y2),(0,0,0),3)
      # jari manis
      length3 = math.hypot(x2-x5,y2-y5)
      if length3 < 50:
        cv2.line(image,(x5,y5),(x2,y2),(0,0,0),3)
      # jari kelingking
      length4 = math.hypot(x2-x6,y2-y6)
      if length4 < 50:
        cv2.line(image,(x6,y6),(x2,y2),(0,0,0),3)
      
      Pos = np.interp(length, [50, 220], [0, 100]) # ibu jari
      Pos1 = np.interp(length1, [50, 220], [0, 100]) # telunjuk
      Pos2 = np.interp(length2, [50, 220], [0, 100]) # jari tengah
      Pos3 = np.interp(length3, [50, 220], [0, 100]) # jari manis
      Pos4 = np.interp(length4, [50, 220], [0, 100]) # jari kelingking

      Posgripper= (round(Pos)) # ibu jari
      Posgripper1= (round(Pos1)) # telunjuk
      Posgripper2= (round(Pos2)) # jari tengah
      Posgripper3= (round(Pos3)) # jari manis
      Posgripper4= (round(Pos4)) # jari kelingking

      # print(Posgripper) # ibu jari
      # print(Posgripper1) # telunjuk
      # print(Posgripper2) # jari tengah
      # print(Posgripper3) # jari manis
      # print(Posgripper4) # jari kelingking
      
      converted_Posgripper = str(Posgripper) # ibu jari
      converted_Posgripper1 = str(Posgripper1) # telunjuk
      converted_Posgripper2 = str(Posgripper2) # jari tengah
      converted_Posgripper3 = str(Posgripper3) # jari manis
      converted_Posgripper4 = str(Posgripper4) # jari kelingking

      cv2.putText(image, str(Posgripper), (30, 60), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0)) # ibu jari
      cv2.putText(image, str(Posgripper1), (30, 100), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0)) # telunjuk
      cv2.putText(image, str(Posgripper2), (30, 140), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0)) # jari tengah
      cv2.putText(image, str(Posgripper3), (30, 180), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0)) # jari manis
      cv2.putText(image, str(Posgripper4), (30, 220), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0)) # jari kelingking

      #cv2.line(image, 320, 320, (0,0,0), 2)
      Servopos=(100-Posgripper) # ibu jari
      Servopos1=(100-Posgripper1) # telunjuk
      Servopos2=(100-Posgripper2) # jari tengah
      Servopos3=(100-Posgripper3) # jari manis
      Servopos4=(100-Posgripper4) # jari kelingking

      print ("Jempol ", Servopos)
    
    cv2.imshow('handDetector', image) 
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
cam.release()