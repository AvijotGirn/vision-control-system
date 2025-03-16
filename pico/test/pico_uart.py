import machine
import utime

# Set up UART (Pico listens on GP1)
uart = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rx=machine.Pin(1))

# Set up LEDs
red_led = machine.Pin(2, machine.Pin.OUT)
blue_led = machine.Pin(3, machine.Pin.OUT)

def control_leds(data):
    """Turn LEDs on/off based on received data."""
    if data == "red":
        red_led.value(1)
        blue_led.value(0)
    elif data == "blue":
        red_led.value(0)
        blue_led.value(1)
    elif data == "both":
        red_led.value(1)
        blue_led.value(1)
    else:  # "none"
        red_led.value(0)
        blue_led.value(0)

while True:
    if uart.any():  # Check if data is available
        data = uart.read().decode('utf-8').strip()  # Read and clean data
        print(f"Received: {data}")
        control_leds(data)  # Control LEDs
    utime.sleep(0.1)
