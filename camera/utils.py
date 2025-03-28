import serial

def get_direction(cx, cy):
    if cx < 100:
        return "left"
    elif cx > 200:
        return "right"
    return "center"


def move_servo(stop_tracking, direction, last_direction, uart):
    if direction != last_direction:
        uart.write((direction + "\n").encode())
        print("Servo Moving: ", direction)
        return direction
    return last_direction

def get_center_position(x, w, y, h):
    return x+w//2, y+h//2
