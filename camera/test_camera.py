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

while True:
    # return value, frame -> read() returns single frame from the video 
    # if ret false, frame could not be captured, i.e cam unplugged
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #define color ranges
    lower_blue = np.array([100, 150, 100])
    upper_blue = np.array([120,255,255])

    lower_red1 = np.array([0,90,90])
    upper_red1 = np.array([10,255,255])

    lower_red2 = np.array([170,90,90])
    upper_red2 = np.array([180,255,255])


    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)

    # check if colors are detected 
    blue_deteced = np.any(mask_blue > 0)
    red_detected = np.any(mask_red > 0)

    cv2.imshow("Camera Feed", frame)
    cv2.imshow("Blue Mask", mask_blue)
    cv2.imshow("Red Mask", mask_red)

    # Wait 1ms for key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
