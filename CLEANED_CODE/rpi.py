from time import sleep
import logging

from paho.mqtt import client as mqtt

import config
import helpers as hp
import marker as mk
import motor
import mqtt_client as mc
import ping

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


def orient_on_qr():
    # DONE_TODO: reorient itself
    frame = mk.get_frame(cap)
    retval = mk.marker_solve(frame)
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
    logging.info("Inside message_callback")
    global cap  # pylint: disable=global-statement
    frame = mk.get_frame(cap)
    new_direction = 'LEFT'
    orient_in_direction(frame, new_direction)
    goto_next_marker()
    orient_on_qr()
    retval = mk.marker_solve(mk.get_frame(cap))
    if retval is None:
        raise Exception("No qr after orient_on_qr finished")
    mc.send_message(client, retval[0].decode("latin-1"))


def main():
    # motor
    motor.setup_motors()

    # ping_Sensor
    ping.setup_ping_sensor()

    # webcam
    global cap  # pylint: disable=global-statement
    cap = mk.setup_webcam()

    # mqtt
    userdata = {"UID": config.UID}
    client_name = str(config.UID)
    client = mqtt.Client(client_name, clean_session=True, userdata=userdata)
    mc.start_mqtt(client, message_callback)

    # DONE_TODO: Initial orientation
    orient_on_qr()
    data, _, _ = mk.marker_solve(mk.get_frame(cap))
    mc.send_message(client, data.decode("latin-1"))
    while True:
        sleep(10)


if __name__ != "__main__":
    raise Exception("This module is not meant to be inherited")
main()
