import time
import config
import RPi.GPIO as GPIO  # pylint: disable=import-error,no-name-in-module


def setup_motors():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(config.RL1, GPIO.OUT)
    GPIO.setup(config.RL2, GPIO.OUT)
    GPIO.setup(config.RL3, GPIO.OUT)
    GPIO.setup(config.RL4, GPIO.OUT)


def start_fw():
    GPIO.output(config.RL1, GPIO.HIGH)
    GPIO.output(config.RL2, GPIO.LOW)
    GPIO.output(config.RL3, GPIO.HIGH)
    GPIO.output(config.RL4, GPIO.LOW)


def start_bw():
    GPIO.output(config.RL1, GPIO.LOW)
    GPIO.output(config.RL2, GPIO.HIGH)
    GPIO.output(config.RL3, GPIO.LOW)
    GPIO.output(config.RL4, GPIO.HIGH)


def start_left():
    GPIO.output(config.RL1, GPIO.LOW)
    GPIO.output(config.RL2, GPIO.HIGH)
    GPIO.output(config.RL3, GPIO.HIGH)
    GPIO.output(config.RL4, GPIO.LOW)


def start_right():
    GPIO.output(config.RL1, GPIO.HIGH)
    GPIO.output(config.RL2, GPIO.LOW)
    GPIO.output(config.RL3, GPIO.LOW)
    GPIO.output(config.RL4, GPIO.HIGH)


def stop():
    GPIO.output(config.RL1, GPIO.LOW)
    GPIO.output(config.RL2, GPIO.LOW)
    GPIO.output(config.RL3, GPIO.LOW)
    GPIO.output(config.RL4, GPIO.LOW)


def drive(direction, duration):
    setup_motors()
    if direction in ['F', 'FORWARD', 0]:
        start_fw()
    elif direction in ['B', 'BACKWARD', 1]:
        start_bw()
    elif direction in ["L", "LEFT", 2]:
        start_left()
    elif direction in ["R", "RIGHT", 3]:
        start_right()
    time.sleep(duration)
    stop()
