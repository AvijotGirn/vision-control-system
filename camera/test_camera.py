import cv2
import numpy as np
import serial
import time

# Open default camera (index 0)
cap = cv2.VideoCapture(0)
uart = serial.Serial("/dev/serial0", baudrate=115200, timeout=1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

cap.set(cv2.CAP_PROP_FPS, 10)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()


 #define color ranges
lower_blue = np.array([100, 150, 100])
upper_blue = np.array([120,255,255])

lower_red1 = np.array([0,90,90])
upper_red1 = np.array([10,255,255])

lower_red2 = np.array([170,90,90])
upper_red2 = np.array([180,255,255])

BLUE_THRESHOLD = 3000
RED_THRESHOLD = 3000

last_sent = ""

while True:
    # return value, frame -> read() returns single frame from the video 
    # if ret false, frame could not be captured, i.e cam unplugged
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)

    # check if colors are detected 
    blue_detected = (np.sum(mask_blue > 0) > BLUE_THRESHOLD)
    red_detected = (np.sum(mask_red > 0) > RED_THRESHOLD)

    if blue_detected and red_detected:
        message = "both"
    elif blue_detected:
        message = "blue"
    elif red_detected:
        message = "red"
    else: 
        message = "none"

    if message != last_sent:
        print(f"Sending: {message}")
        uart.write((message + "\n").encode())
        last_sent = message


    cv2.imshow("Camera Feed", frame)
    cv2.imshow("Blue Mask", mask_blue)
    cv2.imshow("Red Mask", mask_red)

    # Wait 1ms for key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
