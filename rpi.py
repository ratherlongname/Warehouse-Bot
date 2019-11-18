from time import sleep
import time
import logging

from paho.mqtt import client as mqtt

import config
import helpers as hp
import marker as mk
import motor
import mqtt_client as mc
import ping
import stepper


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
    global cap
    cap.release()
    logging.info("Inside goto_next_marker")
    #motor.start_fw()
    motor.drive("F", 0.5)
    retval = None
    cap = mk.setup_webcam()
    while retval is None:
        motor.drive("F", 0.1)
        mk.get_frame(cap)
        print("Chala", retval)
        retval = mk.marker_solve(mk.get_frame(cap))
        png = ping.get_distance()
        print("PING", retval)
        if png < config.MIN_DIST:
            while png < config.MIN_DIST:
                logging.info("Ping distance < %s", config.MIN_DIST)
                cap.release()
                sleep(2000)
                cap =  mk.setup_webcam()
                png = ping.get_distance()
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


def message_callback(client, userdata, message):
    print("Inside message_callback", message.payload)
    pl = message.payload.decode("latin-1")
    global cap  # pylint: disable=global-statement
    frame = mk.get_frame(cap)
    if pl == "UP":
        print("UP")
        stepper.platform_up()
    elif pl == "DOWN":
        print("DOWN")
        stepper.platform_down()
    else:
        orient_in_direction(frame, pl)
        retval = goto_next_marker()
        orient_on_qr(retval)
        #retval = mk.marker_solve(frame)
        if retval is None:
            raise Exception("No qr after orient_on_qr finished")
        mc.send_message(client, retval[0].decode("latin-1"))


def main():
    # motor
    motor.setup_motor()

    # ping_Sensor
    ping.setup_ping_sensor()

    # webcam
    global cap  # pylint: disable=global-statement
    cap = mk.setup_webcam()

    # mqtt
    # userdata = {"UID": config.UID}
    client_name = str(config.UID)
    client = mqtt.Client(client_name, clean_session=True) #, userdata=userdata)
    mc.start_mqtt(client, message_callback)

    # DONE_TODO: Initial orientation
    stepper.setup_stepper()
    retval = mk.marker_solve(mk.get_frame(cap))
    orient_on_qr(retval)
    mc.send_message(client, str(int(retval[0])))
    while True:
        sleep(10)


if __name__ != "__main__":
    raise Exception("This module is not meant to be inherited")
main()
