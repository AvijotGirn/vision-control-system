import time
from machine import Pin, PWM

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

set_servo_duty(LEFT_DUTY)
time.sleep(1)

set_servo_duty(STOP_DUTY)
time.sleep(2)

set_servo_duty(RIGHT_DUTY)
time.sleep(1)

set_servo_duty(STOP_DUTY)
print("Servo stopped")
    
