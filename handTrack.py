import mediapipe as mp
import cv2

class featureDetector():
    def __init__(self, m=False, maxHands=2, detectionConfidence=.6, trackingConfidence=.4):
        self.mode=m
        self.maxHands=maxHands
        self.detectionCon=detectionConfidence
        self.trackCon=trackingConfidence
        self.mpHands=mp.solutions.hands
        self.hands=self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon) #murtaza hand tracking 7:33 might need to turn these up
        self.mpDraw=mp.solutions.drawing_utils
        


    def getFeature(self,frame):
        features=[]
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result=self.hands.process(imgRGB)
        if result.multi_hand_landmarks:
            for hand in result.multi_hand_landmarks:
                for id, lm in enumerate(hand.landmark):
                    h,w,c = frame.shape
                    px, py = int(lm.x*w),int(lm.y*h)
                    features.append((px,py))
                    
                try:    
                    self.mpDraw.draw_landmarks(frame, hand)
                except:
                    pass
            return features

    


# def main():
#     cap=cv2.VideoCapture(0)
#     a=featureDetector()
#     while True:
#         success, frame=cap.read()
#         if success:
#             a.getFeature(frame)
#             cv2.imshow("track", frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             cv2.destroyAllWindows()
#             break
#     cap.release()






# if __name__ == "__main__":
#     main()