import config
import time
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


def menu():
	try:
		main_menu = ['q to quit',
					 'f to go FW',
					 'b to go BW',
					 'l to turn left',
					 'r to turn right',
					 's to stop']
		setup_motors()
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
				if choice == 'q':
					return
				elif choice == 'f':
					start_fw()
				elif choice == 'b':
					start_bw()
				elif choice == 'l':
					start_left()
				elif choice == 'r':
					start_right()
				elif choice == 's':
					stop()
	finally:
		GPIO.cleanup()
	return


if __name__ == "__main__":
	menu()
