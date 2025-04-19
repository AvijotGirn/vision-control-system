# Vision Control System 
A colour-detection motion tracking camera system mounted on a SpringRC Servo.
> This project is a subset of a planned larger robotics system

## Features/Purpose
The purpose of this repository is moreso to track my learning and progress throughout a much larger robotics system project. This project is likely to change (in terms of functionality) throughout its lifecycle, however by keeping a structured format of my findings and milestones, I will be able to refer back at a later time and make changes as required, with all the previous explanation already set out.

Some features of this mini-project include: 
- Color Detection (set to Blue for now)
- UART Communication with RPi Pico
- Continuous Servo control based on commands received via UART (from Pi2B)
- Live feed showing the camera's view
- Key mapping to stop or start tracking 

# Prerequisites

## Materials 
- Raspberry Pi Pico (or equivalent)
- Jumper Cables M2M
- Continuous Rotation Servo (eg. SpringRC SM-S4315R)
- Raspberry Pi 2 Model B (would not recommend anything less)
- USB Camera
- T-Cobbbler
  - 40-pin Ribbon Cable

## Software 
- Raspberry Pi2B setup (Internet connectivity, HDMI, Development Environment, etc...)
- The Python scripts provided in this repo alongside the necessary libraries (OpenCV, Numpy, pyserial)

## Circuit 
![Circuit Schematic](/Images/circ-schematic.png "Circuit Diagram")

## Running 
- Ensure circuit matches the schematic provided above
- With the Pi2 running, ensure the USB camera is connected to it
- Mount the camera to the servo (I used a simple platform screwed onto the servo horn)
  
On the Pico:
- Run the `servo-control.py` script from the `pico/` directory

On the Pi2B:
- Navigate to the `camera/` directory
- Run the `test_camera.py` script
- Wait for camera feed to load

- The tracking should activated on launch
- To disable it, hit the `s` key
- To quit the program, hit the `q` key

## Some Notes
- The `test/` directories are there as progress trackers, making note of small milestones that could potentially come in handy in future projects, they can be safely ignored
- Currently, the program is set to detect blue objects (once a specific threshold or amount of blue is detect on screen)
- Furthermore, considering that I am working with a Pi 2B (weak), the camera resolution is manually set to 320x240, and the framerate to 10 FPS
  - With better hardware this could be run at a much smoother rate/resolution
- `constants.py` can be used to tweak the color ranges (if you would like to test with different colors)
