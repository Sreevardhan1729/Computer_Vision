import cv2
import time
import numpy as np

cap = cv2.VideoCapture(0)

time.sleep(3)
background = 0
for i in range(60):
    ret, background = cap.read()

background = np.flip(background,axis=1)

while(cap.isOpened()):
    ret, img = cap.read()

    if not ret:
        break

    img = np.flip(img,axis=1)
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 120, 80])  # Adjust the saturation and value ranges to be more specific
    upper_red = np.array([10, 255, 255])

    mask1 = cv2.inRange(hsv,lowerb=lower_red,upperb=upper_red)

    lower_red2 = np.array([170, 120, 80])
    upper_red2 = np.array([180, 255, 255])

    mask2 = cv2.inRange(hsv,lowerb=lower_red,upperb=upper_red)
    mask1 = mask1+mask2

    mask1 = cv2.morphologyEx(mask1,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    mask1 = cv2.morphologyEx(mask1,cv2.MORPH_DILATE,np.ones((3,3),np.uint8))

    mask2 = np.bitwise_not(mask1)

    mask1_2d = cv2.merge([mask1,mask1,mask1])
    mask2_2d = cv2.merge([mask2,mask2,mask2])

    res1 = np.bitwise_and(img,img,mask2_2d)
    res2 = np.bitwise_and(background,background,mask1_2d)

    final_output = cv2.addWeighted(res1,1,res2,0.5,0)

    cv2.imshow("Magic",final_output)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()