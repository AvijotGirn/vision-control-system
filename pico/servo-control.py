from machine import Pin, PWM, UART
import time

# Setup UART for receiving commands from Pi
uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))  # GPIO 0 and GPIO 1

# Setup Servo
servo_pin = Pin(15)
servo = PWM(servo_pin)
servo.freq(50)

# Define PWM duty cycle ranges for continuous servo
STOP_DUTY = 1500  # Neutral position → stop rotation
LEFT_DUTY = 1300  # Rotate left
RIGHT_DUTY = 1700  # Rotate right

# Function to set the servo speed/direction
def set_servo_duty(duty_us):
    duty = int(duty_us * 65535 / 20000)  # Scale to 16-bit duty
    servo.duty_u16(duty)

# Start by stopping the servo
set_servo_duty(STOP_DUTY)
print("Servo initialized and stopped")

while True:
    if uart.any():
        command = uart.readline().decode('utf-8').strip()
        print("Received:", command)

        if command == "left":
            set_servo_duty(LEFT_DUTY)
            print("Servo moving left")

        elif command == "right":
            set_servo_duty(RIGHT_DUTY)
            print("Servo moving right")

        elif command == "center":
            set_servo_duty(STOP_DUTY)
            print("Servo stopped")

    time.sleep(0.05)
