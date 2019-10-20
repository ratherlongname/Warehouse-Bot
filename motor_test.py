#!/usr/bin/env python

# Import required modules
import time
import RPi.GPIO as GPIO

# Declare the GPIO settings
GPIO.setmode(GPIO.BOARD)

# set up GPIO pins
GPIO.setup(11, GPIO.OUT) # Connected to RL1
GPIO.setup(12, GPIO.OUT) # Connected to RL2
GPIO.setup(15, GPIO.OUT) # Connected to RL3
GPIO.setup(16, GPIO.OUT) # Connected to RL4

# Drive the motor BW
# Motor A:
GPIO.output(11, GPIO.HIGH) # Set RL1
GPIO.output(12, GPIO.LOW) # Set RL2
# Motor B:
GPIO.output(15, GPIO.HIGH) # Set RL3
GPIO.output(16, GPIO.LOW) # Set RL4

# Wait 5 seconds
time.sleep(5)

# Drive the motor FW
# Motor A:
GPIO.output(11, GPIO.LOW) # Set RL1
GPIO.output(12, GPIO.HIGH) # Set RL2
# Motor B:
GPIO.output(15, GPIO.LOW) # Set RL3
GPIO.output(16, GPIO.HIGH) # Set RL4

# Wait 5 seconds
time.sleep(5)

# Drive the motor CCW
# Motor A:
GPIO.output(11, GPIO.HIGH) # Set RL1
GPIO.output(12, GPIO.LOW) # Set RL2
# Motor B:
GPIO.output(15, GPIO.LOW) # Set RL3
GPIO.output(16, GPIO.HIGH) # Set RL4

# Wait 5 seconds
time.sleep(5)

# Reset all the GPIO pins by setting them to LOW
GPIO.output(12, GPIO.LOW) # Set AIN1
GPIO.output(11, GPIO.LOW) # Set AIN2
GPIO.output(15, GPIO.LOW) # Set BIN1
GPIO.output(16, GPIO.LOW) # Set BIN2