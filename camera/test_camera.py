import cv2
import numpy as np
import serial
from utils import *
from constants import *

# UART setup
# NOTE: You may need to change the serial port below, depending on what is default or setup on your Pi, mine was '/dev/serial0'
uart = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=1)
last_direction = None  #reduce number of calls to uart if last direction is the same as current

# Open default camera (index 0)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv2.CAP_PROP_FPS, 10)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

stop_tracking = False 

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask_blue = cv2.inRange(hsv, LOWER_BLUE, UPPER_BLUE)

    contours, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours: 
        largest_contour = max(contours, key=cv2.contourArea)

        x, y, w, h = cv2.boundingRect(largest_contour)
    
        if w >= MIN_WIDTH and h > MIN_HEIGHT:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255),2)
            cx, cy = get_center_position(x,w,y,h)

            if not stop_tracking:
                direction = get_direction(cx,cy)
                last_direction = move_servo(stop_tracking, direction, last_direction, uart)

        else:
            uart.write(("center" + "\n").encode())
            last_direction = "center"
    else:
        uart.write(("center" + "\n").encode())
        last_direction = "center"

    cv2.imshow("Camera Feed", frame)
    cv2.imshow("Blue Mask", mask_blue)

    if cv2.waitKey(1) & 0xFF == ord('s'):
        uart.write(("center" + "\n").encode())
        stop_tracking = not stop_tracking

    # Wait 1ms for key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
