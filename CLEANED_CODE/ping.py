import time
import config
import RPi.GPIO as GPIO  # pylint: disable=import-error,no-name-in-module


def ping_time_to_distance(ping_time):
    # in cm
    return ping_time * config.TIME_TO_DIST_MULTIPLIER


def trigger_ping_sensor():
    GPIO.output(config.TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(config.TRIGGER, False)


def get_ping_time():
    start_time = 0.0
    stop_time = 0.0
    while GPIO.input(config.ECHO) == 0:
        start_time = time.time()
    while GPIO.input(config.ECHO) == 1:
        stop_time = time.time()
    return stop_time - start_time


def setup_ping_sensor():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(config.TRIGGER, GPIO.OUT)
    GPIO.setup(config.ECHO, GPIO.IN)


def get_distance():

    setup_ping_sensor()
    trigger_ping_sensor()
    ping_time = get_ping_time()
    distance = ping_time_to_distance(ping_time)
    return distance
