import config
import time
import RPi.GPIO as GPIO

def setup_motors():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(config.RL1, GPIO.OUT)
    GPIO.setup(config.RL2, GPIO.OUT)
    GPIO.setup(config.RL3, GPIO.OUT)
    GPIO.setup(config.RL4, GPIO.OUT)
    return

def start_fw():
    GPIO.output(config.RL1, GPIO.HIGH)
    GPIO.output(config.RL2, GPIO.LOW)
    GPIO.output(config.RL3, GPIO.HIGH)
    GPIO.output(config.RL4, GPIO.LOW)
    return

def start_bw():
    GPIO.output(config.RL1, GPIO.LOW)
    GPIO.output(config.RL2, GPIO.HIGH)
    GPIO.output(config.RL3, GPIO.LOW)
    GPIO.output(config.RL4, GPIO.HIGH)
    return

def start_left():
    GPIO.output(config.RL1, GPIO.LOW)
    GPIO.output(config.RL2, GPIO.HIGH)
    GPIO.output(config.RL3, GPIO.HIGH)
    GPIO.output(config.RL4, GPIO.LOW)
    return

def start_right():
    GPIO.output(config.RL1, GPIO.HIGH)
    GPIO.output(config.RL2, GPIO.LOW)
    GPIO.output(config.RL3, GPIO.LOW)
    GPIO.output(config.RL4, GPIO.HIGH)
    return

def stop():
    GPIO.output(config.RL1, GPIO.LOW)
    GPIO.output(config.RL2, GPIO.LOW)
    GPIO.output(config.RL3, GPIO.LOW)
    GPIO.output(config.RL4, GPIO.LOW)
    return

def drive(direction, duration):
    if direction is 'f':
        start_fw()
    elif direction is 'b':
        start_bw()
    elif direction is 'l':
        start_left()
    elif direction is 'r':
        start_right()

    time.sleep(duration)
    stop()
    return

def menu():
    main_menu = ['q to quit',
                'f to go FW',
                'b to go BW',
                'l to turn left',
                'r to turn right',
                's to stop']
    while True:
        print("\tMOTOR TEST MENU")
        print("enter direction and duration (optional)")
        for option in main_menu:
            print(option)
        print("Example:f (start going fw), f 2 (go fw for 2 sec), l 0.5 (turn left for 0.5 sec), s (stop moving) etc. ")

        choice = input()
        try:
            direction, duration = choice.split()
            duration = int(duration)
            drive(direction, duration)
        except ValueError:
            if choice is 'q':
                return
            elif choice is 'f':
                start_fw()
            elif choice is 'b':
                start_bw()
            elif choice is 'l':
                start_left()
            elif choice is 'r':
                start_right()
            elif choice is 's':
                stop()
    return

if __name__ == "__main__":
    setup_motors()
    menu()