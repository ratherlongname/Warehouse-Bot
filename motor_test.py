import config
import time
import RPi.GPIO as GPIO

def setup_motors():
    # Declare the GPIO settings
    GPIO.setmode(GPIO.BOARD)
    # Set GPIO pins
    GPIO.setup(config.RL1, GPIO.OUT)
    GPIO.setup(config.RL2, GPIO.OUT)
    GPIO.setup(config.RL3, GPIO.OUT)
    GPIO.setup(config.RL4, GPIO.OUT)
    return

def reset_all_to_low():
    # Reset all the GPIO pins by setting them to LOW
    GPIO.output(config.RL1, GPIO.LOW)
    GPIO.output(config.RL2, GPIO.LOW)
    GPIO.output(config.RL3, GPIO.LOW)
    GPIO.output(config.RL4, GPIO.LOW)
    return

def drive(direction, duration=1):
    if direction is 'f':
        # Drive the motor FW
        # Motor A:
        GPIO.output(config.RL1, GPIO.HIGH)
        GPIO.output(config.RL2, GPIO.LOW)
        # Motor B:
        GPIO.output(config.RL3, GPIO.HIGH)
        GPIO.output(config.RL4, GPIO.LOW)
        # Go FW for duration
        time.sleep(duration)
    elif direction is 'b':
        # Drive the motor BW
        # Motor A:
        GPIO.output(config.RL1, GPIO.LOW)
        GPIO.output(config.RL2, GPIO.HIGH)
        # Motor B:
        GPIO.output(config.RL3, GPIO.LOW)
        GPIO.output(config.RL4, GPIO.HIGH)
        # Go BW for duration
        time.sleep(duration)
    elif direction is 'l':
        # Turn left
        # Motor A:
        GPIO.output(config.RL1, GPIO.LOW)
        GPIO.output(config.RL2, GPIO.HIGH)
        # Motor B:
        GPIO.output(config.RL3, GPIO.HIGH)
        GPIO.output(config.RL4, GPIO.LOW)
    elif direction is 'r':
        # Turn right
        # Motor A:
        GPIO.output(config.RL1, GPIO.HIGH)
        GPIO.output(config.RL2, GPIO.LOW)
        # Motor B:
        GPIO.output(config.RL3, GPIO.LOW)
        GPIO.output(config.RL4, GPIO.HIGH)

    time.sleep(duration)
    reset_all_to_low()
    return

def menu():
    main_menu = ['q to quit',
                'f to go FW',
                'b to go BW',
                'l to turn left',
                'r to turn right']
    while True:
        print("\tMOTOR TEST MENU")
        print("enter direction and duration (defaults to 1 sec)")
        for option in main_menu:
            print(option)
        print("Example:f, f 2, l 0.5 etc. ")

        choice = input()
        try:
            direction, duration = choice.split()
            drive(direction, duration)
        except ValueError:
            if choice is 'q':
                return
            else:
                drive(choice)
    return

if __name__ == "__main__":
    setup_motors()
    menu()