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


def get_distance_stream():
    try:
        while True:
            distance_in_cm = get_distance()
            print("Measured distance = %.1f cm" % distance_in_cm)
            time.sleep(config.DIST_CHECK_DELAY)
    except KeyboardInterrupt:
        pass
    return


def setup_ping_sensor():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(config.TRIGGER, GPIO.OUT)
    GPIO.setup(config.ECHO, GPIO.IN)
    return


def menu():
    try:
        main_menu = ['q to quit',
                     'd to get distance',
                     's to get distance stream']
        setup_ping_sensor()
        while True:
            print("\tPING SENSOR TEST MENU")
            for option in main_menu:
                print(option)

            choice = input()
            if choice is 'q':
                return
            elif choice is 'd':
                distance_in_cm = get_distance()
                print("Measured distance = %.1f cm" % distance_in_cm)
            elif choice is 's':
                get_distance_stream()
    finally:
        GPIO.cleanup()
    return


if __name__ == '__main__':
    menu()
