import mediapipe as mp
import cv2
from time import sleep
# cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)

mpHands=mp.solutions.hands
hands=mpHands.Hands(False, 1, .6, .5) #murtaza hand tracking 7:33 might need to turn these up
mpDraw=mp.solutions.drawing_utils

cap=cv2.VideoCapture(0)
while True:
    success, frame=cap.read()
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result=hands.process(imgRGB)
    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            for id, lm in enumerate(hand.landmark):
                h,w,c = frame.shape
                px, py = int(lm.x*w),int(lm.y*h)
                
            mpDraw.draw_landmarks(frame, hand, mpHands.HAND_CONNECTIONS)

    cv2.imshow("track", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

cap.release()