from time import sleep
import config, cv2
import helpers as hp
import marker as mk
import motor
import ping
import stepper
import RPi.GPIO as  GPIO
cv2.namedWindow("a", cv2.WINDOW_NORMAL)
GPIO.setwarnings(False)
def show(frame):
    cv2.imshow("a", frame)

cap = None
cap = None

logging.basicConfig()

def orient_in_direction(frame, new_direction):
    logging.info("Inside orient_in_direction")
    # DONE_TODO: rotate in new direction
    retval = mk.marker_solve(frame)
    if retval is None:
        raise Exception("No qr in orient_in_direction")
    _, top, center = retval
    orient_deg = hp.taninv(top[0] - center[0], top[1] - center[1])
    new_direction = config.ANGLES[hp.get_direction_from_name(new_direction)]
    rot_dir, rot_angle = hp.get_rotation_info(orient_deg, new_direction)
    logging.debug("Going %s to %s degrees orient_in_direction", orient_deg, new_direction)
    motor.drive(rot_dir, rot_angle * config.DELAY_PER_ANGLE)


def goto_next_marker():
    # DONE_TODO: goto new location
    logging.info("Inside goto_next_marker")
    motor.start_fw()
    retval = None
    while retval is None:
        sleep(10)
        retval = mk.marker_solve(mk.get_frame(cap))
        if ping.get_distance() < config.MIN_DIST:
            while ping.get_distance() < config.MIN_DIST:
                motor.stop()
                logging.info("Ping distance < %s", config.MIN_DIST)
                sleep(2000)
    return retval


def orient_on_qr(retval):
    # DONE_TODO: reorient itself
    #frame = mk.get_frame(cap)
    #retval = mk.marker_solve(frame)
    if retval is None:
        raise Exception("Not standing on qr but orient_on_qr is called")
    _, top, center = retval
    orientx, orienty = top[0] - center[0], top[1] - center[1]
    orient_deg = hp.taninv(orienty, orientx)
    #! orient_hor, orient_vert = 1024 - center[0], 768 - center[1]
    direction_name, rotation_direction, rot_deg = hp.get_nearest_direction(orient_deg)
    logging.debug("Going %s to %s degrees orient_on_qr",
                  orient_deg, direction_name)
    motor.drive(rotation_direction, rot_deg * config.DELAY_PER_ANGLE)

def message_callback(message):
    global cap  # pylint: disable=global-statement
    frame = mk.get_frame(cap)
    if message.payload == "UP":
        stepper.platform_up()
    elif message.payload == "DOWN":
        stepper.platform_down()
    else:
        orient_in_direction(frame, message.payload)
        goto_next_marker()
        orient_on_qr()
        retval = mk.marker_solve(mk.get_frame(cap))
        if retval is None:
            raise Exception("No qr after orient_on_qr finished")
        print(f"SENDING MQTT {retval[0]}")


def main():
    GPIO.cleanup()
    # motor
    motor.setup_motor()

    # ping_Sensor
    ping.setup_ping_sensor()

    # webcam
    global cap  # pylint: disable=global-statement
    cap = mk.setup_webcam()

    # DONE_TODO: Initial orientation
    #orient_on_qr()
    goto_next_marker()
    #orient_in_direction(mk.get_frame(cap), 1)
    #data, _, _ = mk.marker_solve(mk.get_frame(cap))
    #print(f"SEND MQTT {data}")
    GPIO.cleanup()

try:
    main()
except:
    GPIO.cleanup()
