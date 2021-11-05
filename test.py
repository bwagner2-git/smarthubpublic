# import cv2
# import time
# print(cv2.__version__)
# img=cv2.imread('pup.jpg')
# # time.sleep(5)
# cap = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop) 
# time.sleep(5)
# ret,frame = cap.read() # return a single frame in variable `frame`
# while(True):
#     cv2.imshow('hi',img)
#     cv2.imshow('cool',ret)

# #     cv2.imshow('img1',frame) #display the captured image
#     if cv2.waitKey(1) & 0xFF == ord('y'): #save on pressing 'y' 
#         cv2.destroyAllWindows()
#         break
# # 

# # cap.release()
import cv2
import time
cap = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop) 
time.sleep(3)
ret,frame = cap.read() # return a single frame in variable `frame`

while(True):
    cv2.imshow('img1',frame) #display the captured image
    if cv2.waitKey(1) & 0xFF == ord('y'): #save on pressing 'y' 
        cv2.imwrite('images/c1.png',frame)
        cv2.destroyAllWindows()
        break

cap.release()