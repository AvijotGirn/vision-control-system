import cv2
import numpy as np

# Open default camera (index 0)
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

cap.set(cv2.CAP_PROP_FPS, 10)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

 #define color ranges
lower_blue = np.array([100, 150, 100])
upper_blue = np.array([120,255,255])

BLUE_THRESHOLD = 3000

MIN_WIDTH = 25
MIN_HEIGHT = 50

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    contours, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours: 
        largest_contour = max(contours, key=cv2.contourArea)

        x, y, w, h = cv2.boundingRect(largest_contour)
    
        if w >= MIN_WIDTH and h > MIN_HEIGHT:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255),2)

    cv2.imshow("Camera Feed", frame)
    cv2.imshow("Blue Mask", mask_blue)

    # Wait 1ms for key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
