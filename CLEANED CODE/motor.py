import time

import config
import RPi.GPIO as GPIO


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
	if direction == 'f':
		start_fw()
	elif direction == 'b':
		start_bw()
	elif direction == 'l':
		start_left()
	elif direction == 'r':
		start_right()
	time.sleep(duration)
	stop()
