import cv2
import numpy as np
import serial

# UART setup
uart = serial.Serial("/dev/serial0", baudrate=115200, timeout=1)
last_direction = None  #reduce number of calls to uart if last direction is the same as current

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

FRAME_COUNT = 0

# Previous object positions
prev_cx, prev_cy = None, None
MOVEMENT_THRESHOLD = 10 #Number of pixels to change before it counts as "movement" 

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
            cx, cy = (x + w) // 2, (y + h) // 2 # calculating center position for the boxed object

            # For moving servo to center camera across left and right movements 
            direction = "center"
            if cx < 100:
                direction = "left"

            elif cx > 220:
                direction = "right"

            if direction != last_direction:
                uart.write((direction + "\n").encode())
                print("Servo Moving: ", direction)
                last_direction = direction

            # For Positional tracking (printing movement to screen, fine tuning, etc...)
            # Euclidean distance
#            if prev_cx is not None and prev_cy is not None:
#                dx = cx - prev_cx
#                dy = cy - prev_cy 
#                distance = np.sqrt(dx**2 + dy**2)

#                 if distance > MOVEMENT_THRESHOLD:
#                     # For now we just consider L,R,U,D movement
#                     if abs(dx) > abs(dy):
#                         if dx > 0:
#                             print("Moving right.")
#                         else:
#                             print("Moving left.")
# 
#                     else: # Mostly vertical movement
#                         if dy > 0:
#                             print("Moving down.")
#                         else:
#                             print("Moving up.")
#             FRAME_COUNT += 1
#             if FRAME_COUNT >= 120:
#                 FRAME_COUNT = 0
# 
#             if FRAME_COUNT % 2 == 0:
#                 prev_cx, prev_cy = cx, cy


    cv2.imshow("Camera Feed", frame)
    cv2.imshow("Blue Mask", mask_blue)

    # Wait 1ms for key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
