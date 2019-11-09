def send_initial_message(starting_pos_qrcode):
    import mqtt_rpi
    mqtt_rpi.send_message(starting_pos_qrcode)
    return

def rpi_message_handler(client, userdata, msg):
    # TODO
    command = msg.payload
    print("Command received: {}".format(command))

    if command is "stay":
        return
    elif command is "fw":
        pass
    elif command is "bw":
        pass
    elif command is "left":
        pass
    elif command is "right":
        pass
    elif command is "uturn":
        pass
    elif command is "up":
        pass
    elif command is "down":
        pass
    return

def start_client():
    import mqtt_rpi
    mqtt_rpi.start_server(rpi_message_handler)

def get_qr_code():
    # TODO
    return "abcdqrcode"

def distance_checker():
    # TODO
    import config
    import time
    import ping
    import RPi.GPIO as GPIO
    try:
        ping.setup_ping_sensor()
        while True:
            time.sleep(config.DIST_CHECK_DELAY)
            distance_in_cm = ping.get_distance()
            if distance_in_cm < config.MIN_DIST:
                import motor
                motor.stop()
    finally:
        GPIO.cleanup()
    return

def start_ping_sensor():
    import threading
    ping_sensor_thread = threading.Thread(target=distance_checker)
    ping_sensor_thread.start()
    return

def generate_uid():
    import mqtt_rpi
    mqtt_rpi.generate_uid()
    return

def run_rpi():
    import motor
    import RPi.GPIO as GPIO

    try:
        generate_uid()
        motor.setup_motors()
        start_ping_sensor()
        starting_pos_qrcode = get_qr_code()
        start_client()
        send_initial_message(starting_pos_qrcode)
        while True:
            print("Running...")
            input()
    finally:
        GPIO.cleanup()
    return

if __name__ == "__main__":
    run_rpi()