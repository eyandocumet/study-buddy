# This file is executed on every boot (including wake-boot from deepsleep)
# Eyan Documet - 5/6/25

from hcsr04 import HCSR04
from machine import Pin, PWM
from time import sleep
from math import atan, degrees

# Initialize sensor and servo
sensor = HCSR04(trigger_pin=26, echo_pin=25, echo_timeout_us=10000)
servo = PWM(Pin(13), freq=50)

# Global variables / parameters
bias = 30 # deg -- Added for user comfort
min_dist = 2 # cm
max_dist = 50 # cm
max_angle = 60 # deg

def set_servo_angle(angle_deg):
    min_duty = 1638
    max_duty = 8192
    angle_deg = 90 - angle_deg # For our configuration, this is correct.
    
    duty = int((angle_deg / 180) * (max_duty - min_duty) + min_duty) # Interpolate angle to duty.
    servo.duty_u16(duty)

while True:
    distance = sensor.distance_cm()

    
    theta = degrees(atan((8 + distance) / 9.5)) - bias
    theta = min(theta,max_angle) # Clamped to 45deg

    if (distance >= min_dist) and (distance <= max_dist): # Experimentally found natura minimum of 2cm
        set_servo_angle(theta)
        print(f"Distance: {distance:.0f} cm, Servo Angle: {theta:.1f}deg")
    elif distance > max_dist: # If user has walked away
        set_servo_angle(0)
        print(f"Distance: {distance:.0f} cm, Servo set to \"Away\" Mode")
    else:
        continue
    sleep(0.20) # Blocking code for smoothness, otherwise, we'd need a control algo