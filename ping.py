import config
import time
import RPi.GPIO as GPIO

def ping_time_to_distance(ping_time):
    # in cm
    return (ping_time * 34300) / 2

def get_ping_time():
    start_time = 0.0
    stop_time = 0.0
    while GPIO.input(config.ECHO) == 0:
        start_time = time.time()
    while GPIO.input(config.ECHO) == 1:
        stop_time = time.time()
    return stop_time - start_time

def trigger_ping_sensor():
    GPIO.output(config.TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(config.TRIGGER, False)
    return

def get_distance():
    trigger_ping_sensor()
    ping_time = get_ping_time()
    distance = ping_time_to_distance(ping_time)
    return distance

def setup_ping_sensor():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(config.TRIGGER, GPIO.OUT)
    GPIO.setup(config.ECHO, GPIO.IN)
    return

def menu():
    try:
        main_menu = ['q to quit',
                    'd to get distance']
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
                print ("Measured distance = %.1f cm" % distance_in_cm)
    finally:
        GPIO.cleanup()
    return


if __name__ == '__main__':
    menu()